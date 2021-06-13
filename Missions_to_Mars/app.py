# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask Instance
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")

# Database

# Create Routes

@app.route("/")
def index():
    destination_mars = mongo.db.collection.find_one()
    print(destination_mars)
    return render_template("index.html",destination_mars = destination_mars)

@app.route("/scrape")
def scrape():
    # Link the function
    mars = scrape_mars.scrape()

    # Information to MongoDB
    mongo.db.collection.update({}, mars, upsert=True)

    # Redirect Home Page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)