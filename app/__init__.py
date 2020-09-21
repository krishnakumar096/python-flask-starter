from flask_restplus import Api
from flask import Blueprint, url_for

from .main.user.controller import api as signup_ns
from .main.user.controller import address_api as address_ns
from .main.user.controller import login_api as signin_ns

# we create a blueprint instance by passing name and import_name.
# API is the main entry point for the application resources and hence needs to be initialized
# with the blueprint
blueprint = Blueprint('api', __name__)


# # if os.environ.get('VCAP_SERVICES'):
@property
def specs_url(self):
    return url_for(self.endpoint('specs'), _external=True, _scheme='http')


Api.specs_url = specs_url

api = Api(blueprint,
          title='FLASK STARTER APPLICATION',
          version='1.0',
          description='This is backend API to create user and sign in',
          security='Bearer Auth',
          authorizations={
              'Bearer Auth': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization'
              }
          }
          )

api.add_namespace(signup_ns)
api.add_namespace(address_ns)
api.add_namespace(signin_ns)
