import folium
from flask import Flask, render_template_string, request
from geopy.geocoders import Nominatim
import random

app = Flask(__name__)

# Function to get the latitude and longitude of a location using Geopy
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="climate_risk_assessment_tool")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Function to generate a random risk level
def get_random_risk():
    return random.choice(["High", "Moderate", "Low"])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location_name = request.form["location"]
        lat, lon = get_coordinates(location_name)
        
        if lat and lon:
            # Generate random risk level
            risk_level = get_random_risk()
            
            # Create a map centered on the location
            map = folium.Map(location=[lat, lon], zoom_start=10)
            folium.Marker(
                [lat, lon],
                popup=f"Risk Level: {risk_level}"
            ).add_to(map)
            
            # Get HTML representation of the map
            map_html = map._repr_html_()
            
            return render_template_string("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Random Risk Analysis</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            text-align: center;
                            background-image: url('https://www.postermywall.com/index.php/art/template/6269e09447e6be78b9d4f051f37eebe6/world-map-zoom-meeting-background-design-template');
                            background-size: cover;
                            background-repeat: no-repeat;
                            background-attachment: fixed;
                        }
                        .container {
                            max-width: 800px;
                            margin: 50px auto;
                            padding: 20px;
                            background-color: rgba(255, 255, 255, 0.9);
                            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                            border-radius: 10px;
                        }
                        input[type="text"] {
                            padding: 10px;
                            width: 80%;
                            margin: 10px 0;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                        }
                        input[type="submit"] {
                            padding: 10px 20px;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                        }
                        input[type="submit"]:hover {
                            background-color: #45a049;
                        }
                        .risk {
                            font-size: 1.2em;
                            font-weight: bold;
                            margin: 10px 0;
                        }
                    </style>
                </head>
                <body>

                    <div class="container">
                        <h1>Random Risk Analysis</h1>
                        <form method="post">
                            <input type="text" name="location" placeholder="Enter location" required>
                            <input type="submit" value="Get Risk Analysis">
                        </form>

                        {% if location %}
                            <h3>Risk Analysis for {{ location }}:</h3>
                            <p class="risk">Risk Level: {{ risk_level }}</p>
                            <h4>Risk Map:</h4>
                            <div>{{ map_html|safe }}</div>
                        {% elif error %}
                            <p class="error">{{ error }}</p>
                        {% endif %}
                    </div>

                </body>
                </html>
            """, location=location_name, risk_level=risk_level, map_html=map_html)
        else:
            return render_template_string("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Random Risk Analysis</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            text-align: center;
                            background-image: url('https://www.postermywall.com/index.php/art/template/6269e09447e6be78b9d4f051f37eebe6/world-map-zoom-meeting-background-design-template');
                            background-size: cover;
                            background-repeat: no-repeat;
                            background-attachment: fixed;
                        }
                        .container {
                            max-width: 800px;
                            margin: 50px auto;
                            padding: 20px;
                            background-color: rgba(255, 255, 255, 0.9);
                            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                            border-radius: 10px;
                        }
                        input[type="text"] {
                            padding: 10px;
                            width: 80%;
                            margin: 10px 0;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                        }
                        input[type="submit"] {
                            padding: 10px 20px;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                        }
                        input[type="submit"]:hover {
                            background-color: #45a049;
                        }
                    </style>
                </head>
                <body>

                    <div class="container">
                        <h1>Random Risk Analysis</h1>
                        <form method="post">
                            <input type="text" name="location" placeholder="Enter location" required>
                            <input type="submit" value="Get Risk Analysis">
                        </form>

                        <p class="error">Location not found. Please try again.</p>

                    </div>

                </body>
                </html>
            """)

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Random Risk Analysis</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    text-align: center;
                    background-image: url('https://www.postermywall.com/index.php/art/template/6269e09447e6be78b9d4f051f37eebe6/world-map-zoom-meeting-background-design-template');
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }
                .container {
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: rgba(255, 255, 255, 0.9);
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                    border-radius: 10px;
                }
                input[type="text"] {
                    padding: 10px;
                    width: 80%;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                input[type="submit"] {
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>

            <div class="container">
                <h1>Random Risk Analysis</h1>
                <form method="post">
                    <input type="text" name="location" placeholder="Enter location" required>
                    <input type="submit" value="Get Risk Analysis">
                </form>
            </div>

        </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)
