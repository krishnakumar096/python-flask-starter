from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Integer, String, ForeignKey, func, or_

from app.main import db
from app.main.address.service import AddressService
from app.config.logger import log
from app.util.common_util import Util
from app.config import constants

class RbaUser(db.Model):
    __tablename__ = 'rba_user'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100))
    mobile = db.Column(String(100))
    email = db.Column(String(100))
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(String(250))
    gender = db.Column(String(8))
    aadhaar_no = db.Column(String(20))
    dob = db.Column(db.DateTime())
    profile_image = db.Column(String(250))
    address_id = db.Column(Integer, ForeignKey('address.id'), nullable=True)
    created_at = db.Column(db.DateTime(), default=Util.current_date_time())
    modified_at = db.Column(db.DateTime(), default=Util.current_date_time())
    modified_by = db.Column(Integer)
    is_active = db.Column(db.Boolean, default=True)

    # this method will add user but we have to commit where we have called this method
    @staticmethod
    def add_user(user):

        # adding address in address table
        result = AddressService.add_address(user['address'])
        if result['status'] is False:
            return { 'status': constants.STATUS_FAIL, 'message': 'Failed to create address' }

        address_id = result['address_id']

        '''encrypt password'''
        password = sha256_crypt.encrypt(user['password'])

        try:
            log.info("adding in user table")
            users = RbaUser(name=user['name'],
                            mobile=user['mobile'],
                            email=user['email'],
                            password=password,
                            gender=user['gender'],
                            aadhaar_no=user['aadhaar_no'],
                            dob=user['dob'],
                            profile_image=user['profile_image'],
                            address_id=address_id)
            db.session.add(users)
            db.session.flush()
            op_object = {
                'status': constants.STATUS_PASS,
                'user_id': users.id,
                'address_id': address_id
            }
        except SQLAlchemyError as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            error = template.format(type(e).__name__, e.args)
            log.error("problem in user table")
            log.error(error)
            op_object = {
                'status': constants.STATUS_FAIL,
                'msg': error
            }

        return op_object

    @staticmethod
    def get_by(**kwargs):
        try:
            return RbaUser.query.filter_by(**kwargs).first()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            log.error(error)
            return False

