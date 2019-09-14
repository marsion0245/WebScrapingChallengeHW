
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
	
	featured_image = scrape_jpl(browser)
	
	mars_weather = scrape_mars_weather(browser)
	
	mars_facts = scrape_mars_facts(browser)
	
	hemisphere_image_urls = scrape_hemisphere_image_urls(browser)
	
	print(hemisphere_image_urls)
	
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
	
	news_list = []
	for item in news_items: 
		news = item.find('div', class_='list_text')
		if news:
			n_date = news.find('div', class_='list_date').text
			n_title = news.find('a').text
			n_teaser = news.find('div', class_='article_teaser_body').text
			#print(f"{n_date}\n{n_title}\n{n_teaser}\n")
			news_list.append({'n_date' : n_date, 'n_title': n_title, 'n_teaser' : n_teaser})
			
	return news_list


def scrape_jpl(browser):
	# Scrape site
	url_jpl = "https://www.jpl.nasa.gov"
	url_jpl_mars = url_jpl + "/spaceimages/?search=&category=Mars"
	browser.visit(url_jpl_mars)

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(browser.html, 'html.parser')

	# Get link to the large featured picture
	featured_pic = soup.find('a', id='full_image')
	url_featured_pic = url_jpl + featured_pic['data-fancybox-href']

	# Open picture in browser
	#browser.visit(url_featured_pic) 

	return url_featured_pic


def scrape_mars_weather(browser):
	# Scrape site
	url_twit = "https://twitter.com/marswxreport?lang=en"
	browser.visit(url_twit)

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(browser.html, 'html.parser')

	# Get current weather
	weather_container = soup.find('div', class_='stream')
	weather_current = weather_container.find('p')
	mars_weather = weather_current.text.strip()
	return mars_weather	
	
	
def scrape_mars_facts(browser):
	# Scrape facts using pandas
	url_mars_facts = "https://space-facts.com/mars/"
	mars_facts_df = pd.read_html(url_mars_facts)[1] # data in second table
	mars_facts_df.columns = ['Parameter', 'Value']
	return mars_facts_df


def scrape_hemisphere_image_urls(browser):
	# Scrape site
	url_usgs = "https://astrogeology.usgs.gov"
	url_usgs_mars = url_usgs + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url_usgs_mars)

	# Create BeautifulSoup object; parse with 'html.parser'
	soup = bs(browser.html, 'html.parser')

	hemisphere_image_urls = []

	# Hemispheres container
	# No need to trigger click, use url to navigate to the page with image info instead
	hemi_container = soup.find('div', id='product-section')
	hemi_items = hemi_container.find_all('div', class_='item')
	for item in hemi_items:
		title = item.find('h3').text
		link = item.find('a')['href']
		browser.visit(url_usgs + link)
		soup = bs(browser.html, 'html.parser')
		downloads = soup.find('div', class_='downloads')
		url = downloads.find('a')['href']
		hemisphere_image_urls.append({'title': title, 'img_url' : url})

	return hemisphere_image_urls


scrape()


