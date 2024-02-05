from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Item, RegisterForm, db, User, LoginForm


views = Blueprint("views", __name__)

@views.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    username = form.username.data
    email = form.email.data
    password1 = form.password1.data
    password2 = form.password2.data
    
    if form.validate_on_submit():
        new_user = User(username=username,
                        email=email,
                        password=generate_password_hash(password1,
                                                        method="pbkdf2:sha256"
                                                        )
                        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", category="success")
        return redirect(url_for("views.login_page"))
    
    if User.query.filter_by(email=email).first():
        flash("Email already exists.", category="danger")
    if User.query.filter_by(username=username).first():
        flash("Username already exists.", category="danger")
    if password1 != password2:
        flash("Passwords do not match.", category="danger")
    
    return render_template("register.html", form=form)

@views.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f"Success! You are logged in as {user.username}.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.market_page"))
            flash("Incorrect password. Try again!", category="danger")
        else:
            flash(f"There is no such user as {username}.", category="danger")
            flash("Please check username or register if you do not have an account.",
                  category="warning")
    return render_template("login.html", form=form)

@views.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("Logged out successfully! Enter your details to login again.",
          category="success")
    return redirect(url_for("views.login_page"))
    
@views.route("/")
@views.route("/home")
@login_required
def home_page():
    return render_template("home.html")

@views.route("/market")
@login_required
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)
