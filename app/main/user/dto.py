
from flask_restplus import Namespace, fields
from app.main.address.dto import AddressDto
from app.util.common_util import Util


class SignupDto:
    api = Namespace('users', description='user related operation')
    users = api.model('users', {
        'name': fields.String(description='user first name', min_length=2, max_length=50),
        'mobile': fields.String(required=True, description='user contact_number', min_length=10, max_length=10),
        'email': fields.String(description='user email'),
        'password': fields.String(discription='admin password'),
        'gender': fields.String(description='user gender', enum=['male', 'female', 'others']),
        'aadhaar_no': fields.String(description='user aadhaar number', required=False),
        'dob': fields.DateTime(max=Util.current_date_time().date()),
        'profile_image': fields.String(required=False),
        'address': fields.Nested(AddressDto.address)
    })

class SigninDto:
    api = Namespace('users', description='user related operation')
    signin = api.model('signin', {
        'email': fields.String(description='user email'),
        'password': fields.String(description='user password')
    })