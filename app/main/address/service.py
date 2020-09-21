from app.main.address.model import Address
from app.config.constants import STATUS_FAIL, STATUS_PASS

class AddressService:

    @staticmethod
    def add_address(address_obj):
        return Address.add_address(address_obj)

    @staticmethod
    def get_address_by_address_obj(address_obj):
        address_detail = {
            "id": address_obj.id,
            "address_line1": address_obj.address_line1,
            "address_line2": address_obj.address_line2,
            "street": address_obj.street,
            "area": address_obj.area,
            "city": address_obj.city,
            "village": address_obj.village,
            "talluka": address_obj.talluka,
            "state": address_obj.state,
            "country": address_obj.country,
            "pin_code": address_obj.pin_code,
        }
        return address_detail

    @staticmethod
    def get_address_by_id(address_id):
        address_obj = Address.get_by(id=address_id)
        if address_obj is None:
            return {}
        return AddressService.get_address_by_address_obj(address_obj)