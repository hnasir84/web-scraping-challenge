# get imports
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# use flask pymongo to set up the connection to the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    # access info from the database
    mars_data = mongo.db.marsData.find_one()
    print(mars_data)
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    # reference to te databse collection (table)
    marsTable = mongo.db.marsData

    # drop table if it exists
    mongo.db.marsData.drop()


    # call scrape mars script
    mars_data = scrape_mars.scrape_all()
    print(mars_data)

    # take the dictionary and load it into mongobd
    marsTable.insert_one(mars_data)
    
    return redirect("/")



if __name__ == "__main__":
    app.run()