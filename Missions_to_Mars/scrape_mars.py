
# Mission to Mars - Web Scraping

# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser

def scrape():
	# Using firefox instead of chrome, chrome on my PC has limitation set by IT
	executable_path = {'executable_path': 'geckodriver.exe'} # chromedriver
	browser = Browser('firefox', **executable_path, headless=False)

	news = scrape_nasa(browser)
	print(len(news))
	
	browser.quit()
	
def scrape_nasa(browser):
	# Scrape NASA Mars News
	url_nasa = "https://mars.nasa.gov/news/"

	# Retrieve page with WerbDriver, not request - complex page buildup
	browser.visit(url_nasa)

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(browser.html, 'html.parser')

	# Collect the latest News Title and Paragraph Text. 
	# Assign the text to variables for later reference.
	news_items = soup.find_all('div', class_='image_and_description_container')
	
	news = []
	for item in news_items: 
		news = item.find('div', class_='list_text')
		if news:
			n_date = news.find('div', class_='list_date').text
			n_title = news.find('a').text
			n_teaser = news.find('div', class_='article_teaser_body').text
			#print(f"{n_date}\n{n_title}\n{n_teaser}\n")
			news.append({'n_date' : n_date, 'n_title': n_title, 'n_teaser' : n_teaser})
			
	return news


scrape()
