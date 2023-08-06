# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelView
from trytond.pool import Pool
from trytond.pyson import Eval, Or, Bool
from trytond.transaction import Transaction
from trytond.modules.stock_package.stock import PackageMixin
#from trytond.modules.product import price_digits

from trytond.i18n import gettext
from trytond.exceptions import UserError


class ShipmentCarrierMixin(PackageMixin):
    """
    Mixin class which implements all the fields and methods required for
    getting shipping rates and generating labels
    """

    is_international_shipping = fields.Function(
        fields.Boolean("Is International Shipping"),
        'get_is_international_shipping', loading="lazy"
    )

    weight = fields.Function(
        fields.Float(
            "Weight", digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits'],
        ),
        'get_weight'
    )
    weight_uom = fields.Function(
        fields.Many2One('product.uom', 'Weight UOM'),
        'get_weight_uom'
    )
    weight_digits = fields.Function(
        fields.Integer('Weight Digits'), 'on_change_with_weight_digits'
    )

    tracking_number = fields.Many2One(
        'shipment.tracking', 'Tracking Number', select=True,
        states={'readonly': Eval('state') == 'done'}, depends=['state']
    )

    shipping_instructions = fields.Text(
        'Shipping Instructions', states={
            'readonly': Eval('state').in_(['cancel', 'done']),
        }, depends=['state']
    )

    available_carrier_services = fields.Function(
        fields.One2Many("carrier.service", None, "Available Carrier Services"),
        getter="get_available_carrier_services"
    )
    carrier_service = fields.Many2One(
        "carrier.service", "Carrier Service", domain=[
            ('id', 'in', Eval('available_carrier_services'))
        ], depends=['available_carrier_services', 'state']
    )
    carrier_cost_method = fields.Function(
        fields.Char('Carrier Cost Method'),
        "get_carrier_cost_method"
    )
    shipping_manifest = fields.Many2One(
        "shipping.manifest", "Shipping Manifest", readonly=True, select=True
    )

    @property
    def carrier_cost_moves(self):
        "Moves to use for carrier cost calculation"
        return []

    @classmethod
    def get_carrier_cost_method(cls, records, name):
        res = {}
        for record in records:
            res[record.id] = record.carrier.carrier_cost_method \
                if record.carrier else None
        return res

    @fields.depends("carrier")
    def on_change_with_carrier_cost_method(self, name=None):
        Model = Pool().get(self.__name__)
        return Model.get_carrier_cost_method([self], name)[self.id]

    @classmethod
    def get_available_carrier_services(cls, records, name):
        res = {}
        for record in records:
            res[record.id] = list(map(int, record.carrier.services)) \
                if record.carrier else []
        return res

    @fields.depends('carrier')
    def on_change_with_available_carrier_services(self, name=None):
        Model = Pool().get(self.__name__)
        return Model.get_available_carrier_services([self], name)[self.id]

    @classmethod
    def get_weight(cls, records, name=None):
        """
        Returns sum of weight associated with each package or
        move line otherwise
        """
        Uom = Pool().get('product.uom')

        res = {}
        for record in records:
            weight_uom = record.weight_uom
            if record.packages:
                res[record.id] = sum([
                    Uom.compute_qty(p.weight_uom, p.weight, weight_uom)
                    for p in record.packages if p.weight
                ])
            else:
                res[record.id] = sum([
                    move.get_weight(weight_uom, silent=True)
                    for move in record.carrier_cost_moves
                ])
        return res

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2

    @classmethod
    def __setup__(cls):
        super(ShipmentCarrierMixin, cls).__setup__()
        cls.carrier_service.states = {
            'readonly': Eval('state') == 'done',
        }
        cls._buttons.update({
            'label_wizard': {
                'invisible': Or(
                    (~Eval('state').in_(['packed', 'done'])),
                    (Bool(Eval('tracking_number')))
                ),
            },
        })
        # Following fields are already there in customer shipment, have
        # them in mixin so other shipment model can also use it.

        #cls.carrier = fields.Many2One('carrier', 'Carrier', states={
        #        'readonly': ~Eval('state').in_(['draft', 'waiting', 'assigned',
        #                'packed']),
        #        },
        #    depends=['state'])
        #cls.cost_currency = fields.Many2One('currency.currency',
        #    'Cost Currency', states={
        #        'invisible': ~Eval('carrier'),
        #        'required': Bool(Eval('carrier')),
        #        'readonly': ~Eval('state').in_(['draft', 'waiting', 'assigned',
        #                'packed']),
        #        }, depends=['carrier', 'state'])
        #cls.cost = fields.Numeric('Cost',
        #    digits=price_digits, states={
        #        'invisible': ~Eval('carrier'),
        #        'readonly': ~Eval('state').in_(['draft', 'waiting', 'assigned',
        #                'packed']),
        #        }, depends=['carrier', 'state'])


        cls.packages.context = {'carrier': Eval('carrier')}
        cls.packages.depends = ['carrier']

    @classmethod
    @ModelView.button_action('shipping.wizard_generate_shipping_label')
    def label_wizard(cls, shipments):
        if len(shipments) == 0:
            raise UserError(gettext('shipping.no_shipments'))
        elif len(shipments) > 1:
            raise UserError(gettext('shipping.too_many_shipments'))

    @classmethod
    def copy(cls, shipments, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['tracking_number'] = None
        return super(ShipmentCarrierMixin, cls).copy(shipments, default=default)

    @classmethod
    def get_is_international_shipping(cls, records, name):
        res = dict.fromkeys([r.id for r in records], False)

        for record in records:
            from_address = record._get_ship_from_address(silent=True)
            delivery_address = None
            if hasattr(record, 'delivery_address'):
                delivery_address = record.delivery_address
            elif hasattr(record, 'contact_address'):
                delivery_address = record.contact_address
            if delivery_address and from_address and \
               from_address.country and delivery_address.country and \
               from_address.country != delivery_address.country:
                res[record.id] = True

        return res

    @fields.depends('delivery_address', 'warehouse')
    def on_change_with_is_international_shipping(self, name=None):
        """
        Return True if international shipping
        """
        Model = Pool().get(self.__name__)
        return Model.get_is_international_shipping([self], name)[self.id]

    def get_weight_uom(self, name):
        """
        Returns weight uom for the shipment
        """
        ModelData = Pool().get('ir.model.data')

        return ModelData.get_id('product', 'uom_pound')

    def _get_ship_from_address(self, silent=False):
        """
        Usually the warehouse from which you ship
        """
        # FIXME: from address is not always warehouse address, something
        # like return shipment or supplier shipment makes warehouse
        # to_address.
        if self.warehouse and self.warehouse.address:
            return self.warehouse.address
        if not silent:
            raise UserError(gettext('shipping.warehouse_address_missing'))

    def allow_label_generation(self):
        """
        Shipment must be in the right states and tracking number must not
        be present.
        """
        if self.state not in ('packed', 'done'):
            raise UserError(gettext('shipping.invalid_state'))

        if self.tracking_number:
            raise UserError(gettext('shipping.tracking_number_already_present'))

        return True

    def _create_default_package(self, box_type=None):
        """
        Create a single stock package for the whole shipment
        """
        Package = Pool().get('stock.package')

        package, = Package.create([{
            'shipment': '%s,%d' % (self.__name__, self.id),
            'box_type': box_type and box_type.id,
            'moves': [('add', self.carrier_cost_moves)],
        }])
        return package

    def get_shipping_rates(self, carriers=None, silent=False):
        """
        Gives a list of rates from carriers provided. If no carriers provided,
        return rates from all the carriers.

        List contains dictionary with following minimum keys:
            [
                {
                    'display_name': Name to display,
                    'carrier_service': carrier.service active record,
                    'cost': cost,
                    'cost_currency': currency.currency active repord,
                    'carrier': carrier active record,
                }..
            ]
        """
        Carrier = Pool().get('carrier')

        if carriers is None:
            carriers = Carrier.search([])

        rates = []
        for carrier in carriers:
            rates.extend(self.get_shipping_rate(carrier=carrier, silent=silent))
        return rates

    def get_shipping_rate(self, carrier, carrier_service=None, silent=False):
        """
        Gives a list of rates from provided carrier and carrier service.

        List contains dictionary with following minimum keys:
            [
                {
                    'display_name': Name to display,
                    'carrier_service': carrier.service active record,
                    'cost': cost,
                    'cost_currency': currency.currency active repord,
                    'carrier': carrier active record,
                }..
            ]
        """
        Company = Pool().get('company.company')

        if carrier.carrier_cost_method == 'product':
            currency = Company(Transaction().context['company']).currency
            rate_dict = {
                'display_name': carrier.rec_name,
                'carrier_service': carrier_service,
                'cost': carrier.carrier_product.list_price,
                'cost_currency': currency,
                'carrier': carrier,
            }
            return [rate_dict]

        return []

    def apply_shipping_rate(self, rate):
        """
        This method applies shipping rate. Rate is a dictionary with
        following minimum keys:

            {
                'display_name': Name to display,
                'carrier_service': carrier.service active record,
                'cost': cost,
                'cost_currency': currency.currency active repord,
                'carrier': carrier active record,
            }
        """
        Currency = Pool().get('currency.currency')

        shipment_cost = rate['cost_currency'].round(rate['cost'])
        if self.cost_currency != rate['cost_currency']:
            shipment_cost = Currency.compute(
                rate['cost_currency'], shipment_cost, self.cost_currency
            )

        self.cost = shipment_cost
        self.cost_currency = rate['cost_currency']
        self.carrier = rate['carrier']
        self.carrier_service = rate['carrier_service']
        self.save()

    def generate_shipping_labels(self, **kwargs):
        """
        Generates shipment label for shipment and saves labels,
        tracking numbers.
        """
        raise UserError(gettext(
                "Shipping label generation feature is not available"
                ))

    @staticmethod
    def default_cost_currency():
        Company = Pool().get('company.company')

        company_id = Transaction().context.get('company')

        return company_id and Company(company_id).currency.id or None

    @property
    def ship_from_address(self):
        return None

    @property
    def ship_to_address(self):
        return None
