# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import json

from decimal import Decimal

from trytond.model import fields, ModelView
from trytond.pool import PoolMeta, Pool
from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.pyson import Eval, Or, Bool
from trytond.transaction import Transaction

from trytond.i18n import gettext
from trytond.exceptions import UserError

from .mixin import ShipmentCarrierMixin


class ShipmentOut(ShipmentCarrierMixin, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    @property
    def carrier_cost_moves(self):
        return [m for m in self.outgoing_moves
            if (m.state != 'cancel' and m.quantity)]

    def on_change_inventory_moves(self):
        with Transaction().set_context(ignore_carrier_computation=True):
            super(ShipmentOut, self).on_change_inventory_moves()

    @classmethod
    def get_weight(cls, records, name=None):

        res = {}
        for shipment in records:
            weight_uom = shipment.weight_uom

            if shipment.packages or (shipment.state in ('packed', 'done')):
                res.update(super(ShipmentOut, cls).get_weight([shipment], name))
                continue

            inventory_moves = [m for m in shipment.inventory_moves
                if (m.state != 'cancel' and m.quantity)]
            res[shipment.id] = sum([
                move.get_weight(weight_uom, silent=True)
                for move in inventory_moves
            ])

        return res

    @classmethod
    def pack(cls, shipments):
        for shipment in shipments:
            if not shipment.packages:
                # No package, create a default package
                shipment._create_default_package()
        super(ShipmentOut, cls).pack(shipments)


class ShippingCarrierSelector(ModelView):
    'View To Select Carrier'
    __name__ = 'shipping.label.start'

    carrier = fields.Many2One("carrier", "Carrier", required=True)
    override_weight = fields.Float("Override Weight", digits=(16, 2))
    no_of_packages = fields.Integer('Number of packages', readonly=True)
    box_type = fields.Many2One(
        "carrier.box_type", "Box Type", domain=[
            ('id', 'in', Eval("available_box_types"))
        ], depends=["available_box_types"]
    )

    shipping_instructions = fields.Text('Shipping Instructions', readonly=True)
    carrier_service = fields.Many2One(
        "carrier.service", "Carrier Service", domain=[
            ('id', 'in', Eval("available_carrier_services"))
        ], depends=["available_carrier_services"]
    )

    available_box_types = fields.Function(
        fields.One2Many("carrier.box_type", None, 'Available Box Types'),
        getter="on_change_with_available_box_types"
    )
    available_carrier_services = fields.Function(
        fields.One2Many("carrier.service", None, 'Available Carrier Services'),
        getter="on_change_with_available_carrier_services"
    )

    @fields.depends('carrier', 'carrier_service', 'box_type')
    def on_change_carrier(self):
        self.carrier_service = None
        self.box_type = None

    @fields.depends("carrier")
    def on_change_with_available_box_types(self, name=None):
        if self.carrier:
            return list(map(int, self.carrier.box_types))
        return []

    @fields.depends("carrier")
    def on_change_with_available_carrier_services(self, name=None):
        if self.carrier:
            return list(map(int, self.carrier.services))
        return []

    @classmethod
    def view_attributes(cls):
        return super(ShippingCarrierSelector, cls).view_attributes() + [
            ('//label[@name="no_of_packages"]', 'states', {
                    'invisible': Bool(Eval('no_of_packages')),
            })
        ]


class SelectShippingRate(ModelView):
    'Select Shipping Rate'
    __name__ = 'shipping.label.select_rate'

    rate = fields.Selection([], 'Select Rate')


class GenerateShippingLabelMessage(ModelView):
    'Generate Labels Message'
    __name__ = 'shipping.label.end'

    tracking_number = fields.Many2One(
        "shipment.tracking", "Tracking number", readonly=True
    )
    message = fields.Text("Message", readonly=True)
    attachments = fields.One2Many(
        'ir.attachment', None, 'Attachments', readonly=True
    )
    cost = fields.Numeric("Cost", digits=(16, 2), readonly=True)
    cost_currency = fields.Many2One(
        'currency.currency', 'Cost Currency', readonly=True
    )


class GenerateShippingLabel(Wizard):
    'Generate Labels'
    __name__ = 'shipping.label'

    #: This is the first state of wizard to generate shipping label.
    #: It asks for carrier, carrier_service, box_type and override weight,
    #: once entered, it move to `next` transition where it saves all the
    #: values on shipment.
    start = StateView(
        'shipping.label.start',
        'shipping.select_carrier_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Continue', 'next', 'tryton-go-next'),
        ]
    )

    #: Transition saves values from `start` state to the shipment.
    next = StateTransition()

    #: Select shipping rates
    select_rate = StateView(
        'shipping.label.select_rate',
        'shipping.select_rate_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Continue', 'generate_labels', 'tryton-go-next', default=True),  # noqa
        ]
    )

    #: Transition generates shipping labels.
    generate_labels = StateTransition()

    #: State shows the generated label, tracking number, cost and cost
    #: currency.
    generate = StateView(
        'shipping.label.end',
        'shipping.generate_shipping_label_message_view_form',
        [
            Button('Ok', 'end', 'tryton-ok'),
        ]
    )

    @property
    def shipment(self):
        "Gives the active shipment."
        Shipment = Pool().get(Transaction().context.get('active_model'))
        return Shipment(Transaction().context.get('active_id'))

    def default_start(self, data):
        """Fill the default values for `start` state.
        """
        UOM = Pool().get('product.uom')
        if self.shipment.allow_label_generation():
            values = {
                'no_of_packages': len(self.shipment.packages),
                'shipping_instructions': self.shipment.shipping_instructions,
            }

        if self.shipment.carrier:
            values.update({
                'carrier': self.shipment.carrier.id,
            })
        if self.shipment.packages:
            package_weights = []
            for package in self.shipment.packages:
                if not package.override_weight:
                    continue
                package_weights.append(
                    UOM.compute_qty(
                        package.override_weight_uom,
                        package.override_weight,
                        self.shipment.weight_uom
                    )
                )
            values['override_weight'] = sum(package_weights)

        if self.shipment.carrier_service:
            values['carrier_service'] = self.shipment.carrier_service.id

        return values

    def transition_next(self):
        Company = Pool().get('company.company')

        shipment = self.shipment
        company = Company(Transaction().context['company'])
        shipment.carrier = self.start.carrier
        shipment.cost_currency = company.currency
        shipment.carrier_service = self.start.carrier_service
        shipment.save()

        if not shipment.packages:
            shipment._create_default_package(self.start.box_type)

        default_values = self.default_start({})
        per_package_weight = None
        if self.start.override_weight and \
                default_values['override_weight'] != self.start.override_weight:
            # Distribute weight equally
            per_package_weight = (
                self.start.override_weight / len(shipment.packages)
            )

        for package in shipment.packages:
            if per_package_weight:
                package.override_weight = per_package_weight
                package.override_weight_uom = shipment.weight_uom
            if self.start.box_type and self.start.box_type != package.box_type:
                package.box_type = self.start.box_type
            package.save()

        # Fetch rates, and fill selection field with result list
        rates = self.shipment.get_shipping_rate(
            self.start.carrier, self.start.carrier_service
        )
        result = []
        for rate in rates:
            json_safe_rate = rate.copy()
            json_safe_rate.update({
                'carrier': json_safe_rate['carrier'].id,
                'carrier_service': json_safe_rate['carrier_service'] and
                json_safe_rate['carrier_service'].id,
                'cost_currency': json_safe_rate['cost_currency'].id,
            })

            # Update when delivery date is not None
            if json_safe_rate.get('delivery_date'):
                json_safe_rate.update({
                    'delivery_date': json_safe_rate[
                        'delivery_date'].isoformat()
                })

            # Update when delivery time is not None
            if json_safe_rate.get('delivery_time'):
                json_safe_rate.update({
                    'delivery_time': json_safe_rate[
                        'delivery_time'].isoformat()
                })

            result.append((
                json.dumps(json_safe_rate), '%s %s %s' % (
                    rate['display_name'],
                    rate['cost'],
                    rate['cost_currency'].code,
                )
            ))

        self.select_rate.__class__.rate.selection = result

        return 'select_rate'

    def default_select_rate(self, field):
        rate = None
        if self.select_rate.__class__.rate.selection:
            rate = self.select_rate.__class__.rate.selection[0][0]
        return {
            'rate': rate
        }

    def transition_generate_labels(self):
        "Generates shipping labels from data provided by earlier states"
        Carrier = Pool().get('carrier')
        CarrierService = Pool().get('carrier.service')
        Currency = Pool().get('currency.currency')

        if self.select_rate.rate:
            rate = json.loads(self.select_rate.rate)
            rate.update({
                'carrier': Carrier(rate['carrier']),
                'carrier_service': rate['carrier_service'] and
                CarrierService(rate['carrier_service']),
                'cost': Decimal(rate['cost']),
                'cost_currency': Currency(rate['cost_currency'])
            })
            self.shipment.apply_shipping_rate(rate)
        self.shipment.generate_shipping_labels()

        return "generate"

    def get_attachments(self):  # pragma: no cover
        """
        Returns list of attachments corresponding to shipment.
        """
        Attachment = Pool().get('ir.attachment')

        return list(map(
            int,
            Attachment.search([
                ('resource.origin.id', 'in', list(map(int, self.shipment.packages)),
                    'shipment.tracking', 'stock.package')
            ])
        ))

    def get_message(self):
        """
        Returns message to be displayed on wizard
        """
        message = 'Shipment labels have been generated via %s and saved as ' \
            'attachments for the tracking number' % (
                self.shipment.carrier.carrier_cost_method.upper()
            )
        return message

    def default_generate(self, data):
        return {
            'tracking_number': self.shipment.tracking_number and
            self.shipment.tracking_number.id,
            'message': self.get_message(),
            'attachments': self.get_attachments(),
            'cost': self.shipment.cost,
            'cost_currency': self.shipment.cost_currency.id,
        }
