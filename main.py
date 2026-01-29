import datetime as dt
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
import os
import mailtrap as mt

# import requests


reviews = [{'author_name': 'Ubair Pandith',
            'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ALV-UjW7weMKnKHXRlmdSb9EdmocCZzoQsla4HcKoQwBYsQTAFwUkB1j=s128-c0x00000000-cc-rp-mo',
            'rating': 5,
            'text': 'Service provided was great and they have very humble staff. Hotels provided were worth more than the price paid and driver-cum-guide was very knowledgeable. 5 Star in every aspect. Each and every aspect of our Kashmir trip was well organized. It’s one of the best Travel Agencies in Kashmir if not the best. Kudos to the whole team, keep it up!!'},
           {'author_name': 'Saima Lone',
            'profile_photo_url': 'https://lh3.googleusercontent.com/a-/ALV-UjV6hcMqeGfkIL46j2_1xEJBOyN_z4tupe5VYUuU5K69WizqcWwY=s128-c0x00000000-cc-rp-mo',
            'rating': 5,
            'text': 'Nice experience with Wanderwell Travels. Our package was budget friendly for 6 nights and 7 days, car was well maintained, driver was polite and experienced. Hotels, houseboat, hospitality and food were very good. We are happy and have nice memories of our Kashmir trip. Thank you so much Wanderwell Travels.'},
           {'author_name': 'Danish Bhat',
            'profile_photo_url': 'https://lh3.googleusercontent.com/a/ACg8ocLomwAwA3zbLRcU6xAP3bZ9_4mMoRdZpDDukB4LbSejvevpmw=s128-c0x00000000-cc-rp-mo',
            'rating': 5, 'text': 'Best travel consultant in J&K.Highly recommended.'},
           {'author_name': 'Bablo kumar',
            'profile_photo_url': 'https://lh3.googleusercontent.com/a/ACg8ocJfVDPrCydMNm_gk044aqZCP1DslysMLLHY_vX553Hi8dtsig=s128-c0x00000000-cc-rp-mo',
            'rating': 5,
            'text': 'Delightful and great experience with Wanderwell Travels. We are sincerely thankful  for making excellent arrangements for our memorable Kashmir visit. Our tour manager namely Burhan Rather was very helpful and cooperative throughout our travel. We visited Srinagar, Pahalgam, Gulmarg and Sonamarg. We had a very good and memorable trip.'},
           {'author_name': 'Santosh Yadav',
            'profile_photo_url': 'https://lh3.googleusercontent.com/a/ACg8ocLwKd-CQ-zNRSuzh2bOwFnkMj2rJPRF4q4ydypVyBGB5dKEySA=s128-c0x00000000-cc-rp-mo',
            'rating': 5,
            'text': 'Recently we had booked for Kashmir trip... Good hotels.. good food.. good hospitality.. and a very good driver cum guide to spend 5-6 days..will surely recommend others..'}]

place_id = os.environ.get('PLACE_ID')
google_api_key = os.environ.get('GOOGLE_API_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['CKEDITOR_SERVE_LOCAL'] = True
ckeditor = CKEditor(app)
Bootstrap5(app)


# class Base(DeclarativeBase):
#     pass
#
#
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
# db = SQLAlchemy(model_class=Base)
# db.init_app(app)


# CONFIGURE TABLES
# class Tour(db.Model):
#     __tablename__ = "tours"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(250), nullable=False)
#     location: Mapped[str] = mapped_column(String(250), nullable=False)
#     time: Mapped[str] = mapped_column(String(250), nullable=False)
#     price: Mapped[str] = mapped_column(String(250), nullable=False)
#     img_url: Mapped[str] = mapped_column(String(250), nullable=False)
#     days: Mapped[str] = mapped_column(Integer, nullable=False)
#     destination: Mapped[str] = mapped_column(String(250), nullable=False)
#     popularity: Mapped[str] = mapped_column(Integer, nullable=False)
#     day1: Mapped[str] = mapped_column(String(3000), nullable=False)
#     day2: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day3: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day4: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day5: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day6: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day7: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day8: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day9: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day10: Mapped[str] = mapped_column(String(3000), nullable=True)
#     day11: Mapped[str] = mapped_column(String(3000), nullable=True)


# with app.app_context():
#     db.create_all()


@app.context_processor
def show_year():
    return {"year": dt.datetime.now().year}


@app.route('/')
def home():
    # popular_tours = db.session.execute(db.select(Tour).where(Tour.popularity < 4)).scalars().all()
    # # reviews = fetch_google_reviews()
    # return render_template("index.html", popular_tours=popular_tours, reviews=reviews)
    return render_template("index.html", reviews=reviews)


# @app.route('/show_tours')
# def show_tours():
#     destination = request.args.get("destination")
#     result = db.session.execute(db.select(Tour).where(Tour.destination == destination))
#     tours = result.scalars().all()
#     return render_template("show_tours.html", tours=tours, destination=destination.title())

@app.route("/show_tours")
def show_tours():
    # Logic removed. The browser handles the "destination" parameter now.
    return render_template("show_tours.html")


@app.route('/tour_details')
def tour_details():
    # tour_id = request.args.get('tour_id')
    # result = db.get_or_404(Tour, tour_id)
    # print(result.title)
    # return render_template("tour_details.html", tour=result)
    return render_template("tour_details.html")


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
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email_address"]
        phone = data["phone"]
        adults = data["adults"]
        children = data["children"]
        accommodation = data["accommodation"]
        user_message = data["message"]
        send_mail(name, email, phone, adults, children, accommodation, user_message)
        return render_template("contact.html", message=True)

    return render_template("contact.html", message=False)


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
    try:
        client.send(mail)
        print(f"✅ Email sent successfully")
        return True

    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False


# def fetch_google_reviews():
#     url = (f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}"
#            f"&fields=reviews&key={google_api_key}")
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("result", {}).get("reviews", [])
#     return []


@app.route("/landing_page", methods=["GET", "POST"])
def landing_page():
    # result = db.session.execute(db.select(Tour).where(Tour.destination == "kashmir"))
    # tours = result.scalars().all()
    # reviews = fetch_google_reviews()
    # if request.method == "POST":
    #     data = request.form
    #     name = data["name"]
    #     email = "No Data"
    #     phone = data["phone"]
    #     adults = data["travellers"]
    #     children = "No Data"
    #     accommodation = "No Data"
    #     user_message = "No Data"
    #     send_mail(name, email, phone, adults, children, accommodation, user_message)
    #     return render_template("kashmir-landing.html", message=True, tours=tours, destination="Kashmir",
    #                            reviews=reviews)

    # return render_template("kashmir-landing.html", message=False, tours=tours, destination="Kashmir", reviews=reviews)
    return render_template("kashmir-landing.html", message=False, reviews=reviews)


@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """
    Handle lead submission from the landing page
    - Validates phone number (required field)
    - Sends email notification via Mailtrap
    - Returns JSON response
    """
    try:
        # Get JSON data from request
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No data received'
            }), 400

        # Validate required field (phone)
        phone = data.get('phone', '').strip()
        if not phone:
            return jsonify({
                'success': False,
                'message': 'Phone number is required'
            }), 400

        # Extract lead information
        lead_data = {
            'name': data.get('name', 'Not provided').strip() or 'Not provided',
            'phone': phone,
            'travelers': data.get('travelers', 'Not specified').strip() or 'Not specified',
        }

        name = lead_data["name"]
        phone = lead_data["phone"]
        adults = lead_data["travelers"]
        email = "No Data"
        children = "No Data"
        accommodation = "No Data"
        user_message = "No Data"

        # Send email notification
        email_sent = send_mail(name, email, phone, adults, children, accommodation, user_message)

        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Thank you for your interest! Our team will contact you within 24 hours.',
                'leadId': dt.datetime.now().strftime('%Y%m%d%H%M%S'),
                'source': data.get('source', 'unknown'),
                'timestamp': data.get('timestamp', dt.datetime.now().isoformat()),
                'page_url': data.get('page_url', 'Not available')
            }), 200
        else:
            # Email failed but we still received the lead (logged to console)
            return jsonify({
                'success': False,
                'message': 'We received your request but there was an issue with notifications. Please call us directly at +91 98765 43210.',
                'leadId': dt.datetime.now().strftime('%Y%m%d%H%M%S')
            }), 200

    except Exception as e:
        print(f"❌ Error processing lead: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again or call us directly.'
        }), 500


@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory('.', 'sitemap.xml')


if __name__ == "__main__":
    app.run(debug=True)
