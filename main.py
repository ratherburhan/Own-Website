import datetime as dt
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import os
import smtplib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


# WTForm for creating a Message
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email_address = StringField("Email Address", validators=[DataRequired("This field cannot be empty"), Email(
        message='Invalid Email address')])
    phone = StringField("Phone", validators=[DataRequired("This field cannot be empty")])
    message = CKEditorField("Message", validators=[DataRequired("This field cannot be empty")])
    submit = SubmitField("Submit Message")


my_email = os.environ.get('my_email')
pwd = os.environ.get('pwd')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class Tour(db.Model):
    __tablename__ = "tours"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    time: Mapped[str] = mapped_column(String(250), nullable=False)
    price: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    days: Mapped[str] = mapped_column(Integer, nullable=False)
    destination: Mapped[str] = mapped_column(String(250), nullable=False)
    popularity: Mapped[str] = mapped_column(Integer, nullable=False)
    day1: Mapped[str] = mapped_column(String(1000), nullable=False)
    day2: Mapped[str] = mapped_column(String(1000))
    day3: Mapped[str] = mapped_column(String(1000))
    day4: Mapped[str] = mapped_column(String(1000))
    day5: Mapped[str] = mapped_column(String(1000))
    day6: Mapped[str] = mapped_column(String(1000))
    day7: Mapped[str] = mapped_column(String(1000))
    day8: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.context_processor
def show_year():
    return {"year": dt.datetime.now().year}


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/show_tours')
def show_tours():
    destination = request.args.get("destination")
    result = db.session.execute(db.select(Tour).where(Tour.destination == destination))
    tours = result.scalars().all()
    return render_template("show_tours.html", tours=tours, destination=destination.title())


@app.route('/tour_details')
def tour_details():
    tour_id = request.args.get('tour_id')
    result = db.get_or_404(Tour, tour_id)
    print(result.title)
    return render_template("tour_details.html", tour=result)


@app.route('/destinations')
def destinations():
    return render_template("destinations.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/cancellation_policy')
def cancellation_policy():
    return render_template("cancellation_policy.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        name = contact_form.name.data
        email = contact_form.email_address.data
        phone = contact_form.phone.data
        user_message = contact_form.message.data
        send_mail(name, email, phone, user_message)
        contact_form = ContactForm(formdata=None)
        return render_template("contact.html", message=True, form=contact_form)
    return render_template("contact.html", message=False, form=contact_form)


def send_mail(name, email, phone, user_message):
    email_msg = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {user_message}"
    company_mail = os.environ.get('company_mail')
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=pwd)
        connection.sendmail(from_addr=my_email,
                            to_addrs=f"{company_mail}",
                            msg=f"Subject:User Contact Details\n\n{email_msg}".encode('utf-8'))


if __name__ == "__main__":
    app.run(debug=True)
