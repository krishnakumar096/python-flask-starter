from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Integer, String, ForeignKey, create_engine

from app.main import db
from app.config.logger import log
from app.util.common_util import Util


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(Integer, unique=True, primary_key=True)
    address_line1 = db.Column(String(100))
    address_line2 = db.Column(String(100))
    street = db.Column(String(100))
    area = db.Column(String(100))
    city = db.Column(String(100))
    state = db.Column(String(100))
    country = db.Column(String(100))
    pin_code = db.Column(String(6))
    modified_at = db.Column(db.DateTime(), default=Util.current_date_time())
    created_at = db.Column(db.DateTime(), default=Util.current_date_time())
    modified_by = db.Column(Integer)
    is_active = db.Column(db.Boolean, default=True)

    @staticmethod
    def add_address(address):
        address_obj = Address(address_line1=address['address_line1'],
                              address_line2=address['address_line2'],
                              street=address['street'],
                              area=address['area'],
                              city=address['city'],
                              state=address['state'],
                              country=address['country'],
                              pin_code=address['pin_code'],
                              )
        try:
            db.session.add(address_obj)
            db.session.flush()
            op_obj = {
                'status': True,
                'message': 'address added ',
                'address_id': address_obj.id
            }
            log.info("Address created successfully")
            return op_obj
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            log.error("Failed to create address in table " + str(error))
            op_obj = {
                'status': False,
                'message': 'Failed to create address ',
            }
            return op_obj

    @staticmethod
    def get_by(**kwargs):
        try:
            return Address.query.filter_by(**kwargs).first()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            log.error('Failed to get address by id '+ str(error))
            return False