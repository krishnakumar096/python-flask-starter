import datetime
from passlib.handlers.sha2_crypt import sha256_crypt
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (create_access_token, create_refresh_token)
from app.main import db
from app.main.address.service import AddressService
from app.main.user.model import RbaUser
from app.config.logger import log
from app.config import constants

class RbaUserService:

    @staticmethod
    def signup(request_body):
        result = RbaUser.add_user(request_body)
        if result['status'] == constants.STATUS_PASS:
            try:
                db.session.commit()
                '''generate token and store it token table'''
                user_detail_for_token = {"user_id": result['user_id']}

                '''generate token and store it token table'''
                expires = datetime.timedelta(days=15)
                access_token = create_access_token(identity=user_detail_for_token, expires_delta=expires)
                refresh_token = create_refresh_token(identity=user_detail_for_token, expires_delta=expires)

                '''preparing response object'''
                response_object = {
                    'status': constants.STATUS_PASS,
                    'message': 'Successfully Signed up',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
                return response_object, constants.HTTP_STATUS_CODE_CREATE
            except SQLAlchemyError as e:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                error = template.format(type(e).__name__, e.args)
                return {'status': constants.STATUS_FAIL, 'message': error}
        else:
            return result

    @staticmethod
    def get_user_data_by_id(id):
        result = RbaUser.get_by(id=id)
        if result:
            user_detail = RbaUserService.get_detail_by_user_obj(result)
            return {'status': constants.STATUS_PASS, 'data': user_detail}, constants.HTTP_STATUS_CODE_RESPONSE_SUCCESS
        else:
            return {'status': constants.STATUS_FAIL, 'message': "No record found"}, constants.HTTP_STATUS_CODE_RECORD_NOT_FOUND

    @staticmethod
    def get_detail_by_user_obj(user_model_obj):
        return {
            'id': user_model_obj.id,
            'name': user_model_obj.name,
            'mobile': user_model_obj.mobile,
            'email': user_model_obj.email,
            'gender': user_model_obj.gender,
            'aadhaar_no': user_model_obj.aadhaar_no,
            'dob': str(user_model_obj.dob),
            'profile_image': user_model_obj.profile_image,
            'address': AddressService.get_address_by_id(user_model_obj.address_id)
        }

    @staticmethod
    def signin(request_body):
        # get user detail
        user_entry = RbaUser.get_by(email=request_body['email'])
        if user_entry is None:
            return {'status': constants.STATUS_FAIL, 'message': 'Invalid email'}, constants.HTTP_STATUS_CODE_FORBIDDEN

        if user_entry.is_active is False:
            return {'status': constants.STATUS_FAIL, 'message': 'User is inactive'}, constants.HTTP_STATUS_CODE_BAD_REQUEST

        """password matching by using passlib"""
        is_password_matched = sha256_crypt.verify(request_body['password'], user_entry.password)

        if is_password_matched is True:
            '''generate token and store it token table'''
            user_detail_for_token = {"user_id": user_entry.id}

            '''generate token and store it token table'''
            expires = datetime.timedelta(days=15)
            access_token = create_access_token(identity=user_detail_for_token, expires_delta=expires)
            refresh_token = create_refresh_token(identity=user_detail_for_token, expires_delta=expires)

            '''preparing response object'''
            response_object = {
                'status': constants.STATUS_PASS,
                'message': 'Successfully Signed In',
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return response_object, constants.HTTP_STATUS_CODE_CREATE
        else:
            response_object = {
                'status': constants.STATUS_FAIL,
                'message': 'Invalid Password'
            }
            return response_object, constants.HTTP_STATUS_CODE_CONFLICT
