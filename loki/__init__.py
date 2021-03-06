from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '60808326457a6384f78964761aaa161c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# This is to suppress SQLAlchemy warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


#   Below import is necessary, even if the linter complains about it.
#   This is because the linter cannot distinguish between imports in a script
#   and imports in a package. The order of the imports is also important.
#   These two imports *had* to happen after initializing db.
from loki import routes
from loki.models import User, Classifier, Report

from flask_admin import Admin
from loki.admin_views import UserView, ClassifierView, ReportView


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

admin = Admin(app, name='Loki Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(UserView(User, db.session))
admin.add_view(ClassifierView(Classifier, db.session))
admin.add_view(ReportView(Report, db.session))
