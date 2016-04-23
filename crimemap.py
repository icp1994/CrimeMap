import json
import datetime
import string
import dateparser
from dbhelper import DBHelper
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB = DBHelper()
categories = ['mugging', 'break-in']


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"

    return ''.join(i for i in userinput if i in whitelist)


@app.route("/")
def home(err_msg=None):
    crimes = json.dumps(DB.get_all_crimes())

    return render_template("home.html",
                           crimes=crimes,
                           categories=categories,
                           err_msg=err_msg)


@app.route("/submitcrime", methods=["POST"])
def submitcrime():
    category = request.form.get('category')
    if category not in categories:
        return home()
    date = format_date(request.form.get('date'))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")
    try:
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
    except ValueError:
        return home()
    description = sanitize_string(request.form.get('description'))

    DB.add_crime(category, date, latitude, longitude, description)

    return redirect("/")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
