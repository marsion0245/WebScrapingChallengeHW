
# Import Flask
from flask import Flask, render_template

#Create an app, pass __name__
app = Flask(__name__)

# Define static routes
@app.route("/")
def home():
    return render_template("index.html", message="Hello Mars Mission!");

@app.route("/scrape")
def scrape_new_data():
    return "Mars project data scraper"

@app.route("/about")
def about():
    return "<div>This is web part of Mission to Mars HW</div><div>Martin Hrbac</div>"

if __name__ == "__main__":
    app.run(debug=True)

