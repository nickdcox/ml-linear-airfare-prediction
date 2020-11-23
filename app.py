"""

US Domestic Airfare Predictor - Flask App v1  
This program is used as part of a Flask web app and uses the Google Maps API.

"""

from flask import Flask, request, render_template
from flask_googlemaps import GoogleMaps, Map
from math import sin, cos, sqrt, atan2, radians

import joblib
from pandas import DataFrame
import csv

app = Flask(__name__)

def dist(nonstop, originLat, originLong, destlat, destLong):
    # approximate radius of earth in km
    R = 6373.0
    
    lat1 = radians(originLat)
    lon1 = radians(originLong)
    lat2 = radians(destlat)
    lon2 = radians(destLong)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c / 1.6
    
    if nonstop == 0:
        distance = distance * 1.5
        
    return distance

# Define Google Maps API key.
GoogleMaps(app, key="AIzaSyCBDpHInB7HK7bI5oQK9JSrD4LzPfV6Epw")

# Load the regression model from the binary file.
regressor = joblib.load('model.sav')

# Load a file containing a mapping of airport codes, including coordinates.
f = open("airport_codes.csv")
rows = csv.reader(f)
next(rows)

airportCodes = {}
airportLat = {}
airportLong = {}
for columns in rows:
    airportCodes[columns[0]] = int(columns[1])
    airportLat[columns[0]] = float(columns[3])
    airportLong[columns[0]] = float(columns[4])                

# Display a blank map when the page is first loaded.
@app.route("/")
def map_created_in_view():

    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=39.5, 
        lng=-98.35,
        zoom=4,
        zoom_control=0,
        fullscreen_control=0,
        maptype_control=0,
        streetview_control=0,
        scrollwheel=0,

        style="height:425px;width:700px;margin:auto;",
    )
    return render_template("index.html", gmap=gmap)

if __name__ == "__main__":
    app.run(port=5050)

# Obtain user inputs and make a prediction of airfare using the loaded model.
@app.route('/predict',methods=['POST'])
def predict():
    
    # Obtain form inputs and build a dataframe to pass to the model.
    int_features = [x for x in request.form.values()]
    
    if len(int_features) < 6:
        int_features.append(0)
    
    month = int(int_features[4])
    quarter = 0
    if(month <= 3):
        quarter = 1
    elif(month <= 6):
        quarter = 2
    elif(month <= 9):
        quarter = 3
    else:
        quarter = 4
        
    originAirport = int_features[0].upper()
    destAirport = int_features[1].upper()
    
    originAirport = airportCodes[originAirport]
    destAirport = airportCodes[destAirport]
    
    originLat = airportLat[int_features[0].upper()]
    originLong = airportLong[int_features[0].upper()]
    destLat = airportLat[int_features[1].upper()]
    destLong = airportLong[int_features[1].upper()]
    
    nonstop = int(int_features[5])
    
    miles = dist(nonstop, originLat, originLong, destLat, destLong)
    
    classType = [0, 0, 0]
    fareClass = int(int_features[3])
    classType[fareClass] = 1
        
    ticketCarrier = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    carrier = int(int_features[2])
    ticketCarrier[carrier] = 1
    
    df = DataFrame([quarter, originAirport, destAirport, miles, nonstop, classType[0], classType[1], classType[2], ticketCarrier[0], ticketCarrier[1], ticketCarrier[2], ticketCarrier[3], ticketCarrier[4], ticketCarrier[5], ticketCarrier[6], ticketCarrier[7], ticketCarrier[8], ticketCarrier[9], ticketCarrier[10]])
    df = DataFrame(df).transpose()
    df.columns = ['QUARTER', 'ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID',
                  'MARKET_MILES_FLOWN', 'NON_STOP', 'FARE_CLASS_Business', 
                  'FARE_CLASS_Coach', 'FARE_CLASS_First', 'TICKET_CARRIER_AA', 
                  'TICKET_CARRIER_AS', 'TICKET_CARRIER_B6', 'TICKET_CARRIER_DL', 
                  'TICKET_CARRIER_F9', 'TICKET_CARRIER_G4', 'TICKET_CARRIER_HA', 
                  'TICKET_CARRIER_NK', 'TICKET_CARRIER_SY', 'TICKET_CARRIER_UA', 
                  'TICKET_CARRIER_WN']
    
    prediction = regressor.predict(df)
    output = round(prediction[0], 2)
    
    # Display an updated map with a line between the origin and destination.
    polyline = {
            "stroke_color": "#000000",
            "stroke_opacity": 1.0,
            "stroke_weight": 2,
            "path": [
                {"lat": originLat, "lng": originLong},
                {"lat": destLat, "lng": destLong},
            ],
            }
    
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=39.5, 
        lng=-98.35,
        zoom=4,
        zoom_control=0,
        fullscreen_control=0,
        maptype_control=0,
        streetview_control=0,
        scrollwheel=0,        
        polylines=[polyline],
        markers=[
            {
                "icon": "//icons.iconarchive.com/icons/icons8/windows-8/32/Transport-Airplane-Takeoff-icon.png",
                "lat": originLat,
                "lng": originLong,
                },
            {
                "icon": "//icons.iconarchive.com/icons/icons8/windows-8/32/Transport-Airplane-Landing-icon.png",
                "lat": destLat,
                "lng": destLong,
                },
            ],
        style="height:425px;width:700px;margin:auto;",
    )    
    return render_template('index.html', prediction_text='Predicted Airfare is $ {0:.2f}'.format(output), gmap=gmap)