import os
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import blueprint, api
from app.main import create_app, db
from flask_jwt_extended import JWTManager
from app.config.config import PythonConfig
import app.main.user.model
import app.main.address.model

# calls the create_app function from main __inti__ to create the application instance
# with the required parameter from the environment variable which can be either of the
# following - dev, prod, test. If none is set in the environment variable, the default  dev is used.
app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

# registering blueprint with the Flask application instance.
app.register_blueprint(blueprint)


app.app_context().push()
CORS(app)

# These two lines instantiates the manager and migrate classes by passing
# the app instance to their respective constructors.
manager = Manager(app)

migrate = Migrate(app, db)

# we pass the db and MigrateCommand instances to the add_command interface of the
# manager to expose all the database migration commands through Flask-Script.
manager.add_command('db', MigrateCommand)

'''Because of JWT refresh_token, access token'''
jwt = JWTManager(app)
jwt._set_error_handler_callbacks(api)

@manager.command
def run():
    app.run(host="0.0.0.0", port=PythonConfig.flask_port)


if __name__ == '__main__':
    manager.run()
