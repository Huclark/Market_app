from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired
from . import db

class RegisterForm(FlaskForm):
    """Registeration form model
    """
    username = StringField(label="Username:", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="Email Address:", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password:", validators=[Length(min=7), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")

class LoginForm(FlaskForm):
    """Login form model
    """
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class User(db.Model, UserMixin):
    """User model
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    budget =db.Column(db.Integer(), nullable=False, default=20000)
    items = db.relationship('Item', backref='user', lazy=True)
    
    @property
    def formatted_budget(self):
        formatted_number = "{:,.2f}".format(self.budget)
        return f"{formatted_number}"
    
    def balance_sufficient(self, item):
        return self.budget >= item.price
        


class Item(db.Model):
    """Item model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def str(self):
        """String representation of model

        Returns:
            str: string representation of model
        """
        return f"Item{self.id}: {self.name}"
    
    def format_price(self, price):
        return "{:,.2f}".format(self.price)
    
class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Purchase Item!")
    
class SellForm(FlaskForm):
    submit = SubmitField(label="Sell Item!")
