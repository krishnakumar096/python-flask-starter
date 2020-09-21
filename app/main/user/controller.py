from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.main.address.dto import AddressDto
from app.main.user.dto import SignupDto
from app.main.user.dto import SigninDto
from app.main.user.service import RbaUserService
from app.config.logger import log

api = SignupDto.api
address_api = AddressDto.api
login_api = SigninDto.api


@api.route('/signup')
class Users(Resource):
    @api.expect(SignupDto.users, validate=True)
    def post(self):
        # converting request into json
        request_body = request.json
        log.info("Request body to create user: %s", request_body)
        response_body = RbaUserService.signup(request_body)
        log.info("Sending response as: %s", response_body)
        return response_body


@api.route('/<int:user_id>')
class GetUser(Resource):
    # @jwt_required
    def get(self, user_id):
        # converting request into json
        log.info("Get user id: %s", user_id)
        response_body = RbaUserService.get_user_data_by_id(user_id)
        log.info("Sending response as:  %s", response_body)
        return response_body


@api.route('/signin')
class UserSignIn(Resource):
    @api.expect(SigninDto.signin, validate=True)
    def post(self):
        request_body = request.json
        log.info("Request body to sign in: %s", request_body)
        response_body = RbaUserService.signin(request_body)
        log.info("Sending response as:  %s", response_body)
        return response_body
