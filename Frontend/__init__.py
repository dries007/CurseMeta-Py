import logging
import mimetypes
import CurseClient

from flask import Flask
from flask_script import Manager

logging.basicConfig(level=logging.WARN)

mimetypes.init()

app = Flask(__name__)
app.config.from_object('config')

if app.config.get('STAGING', False):
    logging.basicConfig(logging=logging.DEBUG)

manager = Manager(app)

curse = CurseClient.CurseClient(app.config['CURSE_USER'], app.config['CURSE_PASS'], app.config['SOAP_CACHE'])

from . import views

# fixme: It's impossible to catch HTTPException. Flask Bug #941 (https://github.com/pallets/flask/issues/941)
from werkzeug.exceptions import default_exceptions
for code, ex in default_exceptions.items():
    app.errorhandler(code)(views.any_error)

