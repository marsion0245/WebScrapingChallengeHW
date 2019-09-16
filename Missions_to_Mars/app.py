# ==============================================
# Mission to Mars - web server portion
# ==============================================

# Dependancy import
from flask import Flask, render_template, redirect
import pymongo

# Scraping code 
from scrape_mars import scrape_all

#Create an app, pass __name__
app = Flask(__name__)

collection_name = "scraped_data"

# Define static routes
@app.route("/")
def home():

	# Get data from database
	# Connect to MongoDB
	connection = 'mongodb://localhost:27017' # default port
	client = pymongo.MongoClient(connection)

	db = client.MissionToMars
	collection = db[collection_name]
	data = collection.find_one()

	return render_template("index.html", marsdata=data)

@app.route("/scrape")
def scrape_new_data():
	print("Web scraping started ...")

	try:
		# Get data
		mission_data = scrape_all()
		
		# Save data in database
		# Connect to MongoDB
		connection = 'mongodb://localhost:27017' # default port
		client = pymongo.MongoClient(connection)

		# Database
		db = client.MissionToMars

		# Delete previous data
		collist = db.list_collection_names()
		if collection_name in collist:
			db[collection_name].drop()

		colection = db[collection_name]
		id = colection.insert_one(mission_data)

	except:
		print("Error during data scraping")
	
	return redirect('/')
	#return "Mars project data scraping finished"

@app.route("/about")
def about():
    return "<div>This is web part of Mission to Mars HW</div><div>Martin Hrbac</div>"

if __name__ == "__main__":
    app.run(debug=True)

