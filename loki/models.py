from loki import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_validator import ValidateEmail

import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """[User]
    Parameters
    ----------
    username: [string]
        Unique username.
    email: [email]
        Unique email.
    image_file: [string]
        File path for the chosen profile picture.
        Default image is default.jpg.
    _password: [string]
        Hashed password.
        Extra functions are there to hash the password then store it.

    Relationships
    -------------
    models: [Model]
        One to many.
        Models uploaded by the user.
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    image_file = db.Column(db.String(30),
                           nullable=False,
                           default='default.jpg')

    _password = db.Column(db.String(128), nullable=False)

    models = db.relationship("FRS", back_populates="user")

    def __init__(self,
                 username, email,
                 password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return (f"User('{self.username}': '{self.email}')")

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    @classmethod
    def __declare_last__(cls):
        # Check available validators:
        # https://flask-validator.readthedocs.io/en/latest/
        # check_deliverability is set to False to avoid a deprecation
        # warning with pytest; this is due to a problem
        # with the flask-validator release available on PyPI.
        # We already contacted the developer to update the release
        # and hopefully we can set the check to True afterwards.
        ValidateEmail(User.email,
                      allow_smtputf8=True,
                      check_deliverability=False,
                      throw_exception=True,
                      message="The e-mail is invalid.")


class FRS(db.Model):
    """[Facial Recognition System]
    Parameters
    ----------
    name: [string]
        User-chosen name that will show in a model-selector later on.
        **Note**: Use werkzeug.utils.secure_filename
        https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.utils.secure_filename
    upload_date: [datetime]
        Upload date.
    file_path: [string]
        Set by the server. File path for the model on the file system.

    Relationships
    -------------
    user: [User]
        Many to one.
        User that uploaded the model.
        **Note**: Shouldn't be nullable.
    reports: [Report]
        One to many.
        All reports generated for the model.
    """
    __tablename__ = "FRS"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), unique=False, nullable=True)
    upload_date = db.Column(db.DateTime,
                            default=datetime.datetime.now)
    # file_path should not be nullable; set to True only for testing
    file_path = db.Column(db.String(50), unique=True, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="models")

    reports = db.relationship("Report", back_populates="model")

    def __init__(self, name, file_path,
                 user):
        self.name = name
        self.file_path = file_path

        self.user = user

    def __repr__(self):
        return(f"FRS('{self.name}') for {self.user},"
               f" uploaded on {self.upload_date}.")


class Report(db.Model):
    """[Report]
    Parameters
    ----------
    date: [datetime]
        Date of report.
    data: [JSON]
        Actual report data.
    model: [Model]
        FRS for which the report is generated.

    Relationships
    -------------
    model: [Model]
        Many to one.
        The model for which the report was generated.
    """
    __tablename__ = "report"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime,
                     default=datetime.datetime.now)

    model_id = db.Column(db.Integer, db.ForeignKey("FRS.id"))
    model = db.relationship("FRS", back_populates="reports")

    data = db.Column(db.JSON)

    def __init__(self, date, model):
        self.date = date
        self.model = model

    def __repr__(self):
        return(f"Report for {self.model}, "
               f"generated on {self.date}.")
