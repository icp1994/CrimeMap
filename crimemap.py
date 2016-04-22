import json
from dbhelper import DBHelper
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():
    crimes = json.dumps(DB.get_all_crimes())

    return render_template("home.html", crimes=crimes)


@app.route("/submitcrime", methods=["POST"])
def submitcrime():
    category = request.form.get('category')
    date = request.form.get('date')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    description = request.form.get('description')

    DB.add_crime(category, date, latitude, longitude, description)

    return redirect("/")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
