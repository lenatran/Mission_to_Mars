# Dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app)


# Create route that renders index.html template
@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info=mars_info)


# Create route that scrapes and updates Mars data
@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape()
    mars_info.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)



if __name__ == "__main__":
    app.run(debug=True)