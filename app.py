import urllib.parse
import requests

from flask import Flask, flash, redirect, render_template, request, session, request
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


APIKey = "5ae2e3f221c38a28845f05b611bcda45a47612003f06c0b8e43b7105"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # get data from form
        destination = request.form.get("destination")
        days = request.form.get("days")
        startTime = request.form.get("checkInTime")
        endTime = request.form.get("checkOutTime")
        preferences = request.form.getlist("preferences")
        repititions = 0

        # Get attractions data
        attractions = locate_attractions(destination, preferences)

        # TODO Organize list of attractions and add lunch options based on time of day

        return render_template("itinerary.html", preferences=preferences, destination=destination, days=days,
                               startTime=startTime, endTime=endTime,
                               attractions=attractions, repititions=repititions)

    else:

        preferenceList = ["adult", "amusements",
                          "architecture",
                          "cultural",
                          "industrial_facilities",
                          "natural",
                          "other",
                          "religion",
                          "sport"]

        return render_template("index.html", preferenceList=preferenceList)


def locate_destination(destination: str) -> dict:
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?name=  \
          {urllib.parse.quote_plus(destination)}&apikey={APIKey}"
    coordinates = {"long": 0, "lat": 0}
    location = requests.get(url)
    location_data = location.json()
    coordinates["long"], coordinates["lat"] = location_data["lon"], location_data["lat"]
    return coordinates


def locate_attractions(destination: str, preferences: list) -> list:
    print(preferences)

    long, lat = locate_destination(destination)["long"], locate_destination(destination)["lat"]
    if preferences:
        preferences_escaped = "%2C".join(preferences)

        url = \
            f"https://api.opentripmap.com/0.1/en/places/radius?radius=90000&lon={long}&lat={lat}&kinds={preferences_escaped} \
            &format=json&limit=50&apikey={APIKey}"

    else:
        url = \
            f"https://api.opentripmap.com/0.1/en/places/radius?radius=90000&lon={long}&lat={lat}\
                &format=json&limit=50&apikey={APIKey}"

    attractions = requests.get(url)
    attractions_data = attractions.json()
    return attractions_data


def locate_accomodations(destination: str) -> str:
    long, lat = locate_destination(destination)["long"], locate_destination(destination)["lat"]
    url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=10000&lon={long}&lat={lat} \
    &kinds=accomodations&format=json&limit=1&apikey={APIKey}"
    accomodation = requests.get(url)
    accomodation_data = accomodation.json()
    return accomodation_data
