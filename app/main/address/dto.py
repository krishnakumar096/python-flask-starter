from flask_restplus import Namespace, fields


class AddressDto:
    api = Namespace('address', description='Address related operations')
    address = api.model('address', {
        'address_line1': fields.String(description='address line 1', default=""),
        'address_line2': fields.String(description='address line 2', default=""),
        'street': fields.String(description='street', required=False, default=""),
        'area': fields.String(description='area', required=False, default=""),
        'city': fields.String(description='city name', default=""),
        'state': fields.String(description='state of address', default=""),
        'country': fields.String(description='country of address', default="India", ),
        'pin_code': fields.String(description='pin code of address', default=""),
    })
