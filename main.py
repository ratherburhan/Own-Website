import datetime as dt
from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField
from postmarker.core import PostmarkClient
import mailtrap as mt


# WTForm for creating a Message
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email_address = EmailField("Email Address", validators=[DataRequired("This field cannot be empty"),
                                                            Email(message="Invalid Email ID")])
    phone = StringField("Phone", validators=[DataRequired("This field cannot be empty")])
    adults = SelectField(label='Adults',
                         choices=["Please choose", 1, 2, 3, 4, 5, 6, 7, 8, 9, '10+'],
                         validators=[DataRequired("This field cannot be empty")])
    children = SelectField(label='Children(5-12 year)', choices=["Please choose", 1, 2, 3, 4, 5, 6, 7, 8, 9, '10+'],
                           validators=[DataRequired("Children(5-12 year)")])
    accommodation = SelectField(label='Select Accommodation',
                                choices=["Please choose", "Budget", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "Luxury"],
                                validators=[DataRequired("This field cannot be empty")])
    message = CKEditorField("Message", validators=[DataRequired("This field cannot be empty")])
    submit = SubmitField("Submit Message")


# my_email = os.environ.get('my_email')
# pwd = os.environ.get('pwd')

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
    day1: Mapped[str] = mapped_column(String(3000), nullable=False)
    day2: Mapped[str] = mapped_column(String(3000), nullable=True)
    day3: Mapped[str] = mapped_column(String(3000), nullable=True)
    day4: Mapped[str] = mapped_column(String(3000), nullable=True)
    day5: Mapped[str] = mapped_column(String(3000), nullable=True)
    day6: Mapped[str] = mapped_column(String(3000), nullable=True)
    day7: Mapped[str] = mapped_column(String(3000), nullable=True)
    day8: Mapped[str] = mapped_column(String(3000), nullable=True)


with app.app_context():
    db.create_all()


@app.context_processor
def show_year():
    return {"year": dt.datetime.now().year}


@app.route('/')
def home():
    popular_tours = db.session.execute(db.select(Tour).where(Tour.popularity < 4)).scalars().all()
    return render_template("index.html", popular_tours=popular_tours)


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
        adults = contact_form.adults.data
        children = contact_form.children.data
        accommodation = contact_form.accommodation.data
        user_message = contact_form.message.data
        send_mail(name, email, phone, adults, children, accommodation, user_message)
        contact_form = ContactForm(formdata=None)
        return render_template("contact.html", message=True, form=contact_form)

    return render_template("contact.html", message=False, form=contact_form)


# def send_mail(name, email, phone, adults, children, accommodation, user_message):
#     text_msg = (f"<p>Name: {name}<br>Email: {email}<br>Phone: {phone}<br>Adults: {adults}<br>Children: {children}"
#                 f"<br>Accommodation: {accommodation}<br><br>Message as follows:<p><br>{user_message}")
#     company_mail = os.environ.get('company_mail')
#
#     postmark = PostmarkClient(server_token=os.environ.get('server_token'))
#     postmark.emails.send(
#         From=company_mail,
#         To=company_mail,
#         Subject='Lead Details',
#         HtmlBody=text_msg
#     )


def send_mail(name, email, phone, adults, children, accommodation, user_message):
    text_msg = (f"<p>Name: {name}<br>Email: {email}<br>Phone: {phone}<br>Adults: {adults}<br>Children: {children}"
                f"<br>Accommodation: {accommodation}<br><br>Message as follows:<p><br>{user_message}")
    company_mail = os.environ.get('company_mail')
    mailtrap_mail = os.environ.get('sender_mail')
    mail = mt.Mail(
        sender=mt.Address(email=mailtrap_mail, name="Mailtrap Lead"),
        to=[mt.Address(email=company_mail)],
        subject="Lead Details",
        html=text_msg,
        category="Sales Mail",
    )
    client = mt.MailtrapClient(token=os.environ.get('token_mail'))
    client.send(mail)


@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory('.', 'sitemap.xml')


if __name__ == "__main__":
    app.run()
