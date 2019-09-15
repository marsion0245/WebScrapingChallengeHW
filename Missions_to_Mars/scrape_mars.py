
# Mission to Mars - Web Scraping
# Due to the issues with handling of time delays during page loading code creates new browser for each scrapted page
# https://buildmedia.readthedocs.org/media/pdf/splinter/latest/splinter.pdf

# Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from time import sleep

def get_browser():
	# Using Firefox instead of Chrome, Chrome on my PC has limitation set by IT
	executable_path = {'executable_path': 'geckodriver.exe'}
	return Browser('firefox', **executable_path, headless=False)

def scrape_all():

	nasa_news = scrape_nasa()
	jpl_featured_image = scrape_jpl()
	mars_weather = scrape_mars_weather()
	mars_facts = scrape_mars_facts()
	hemisphere_image_urls = scrape_hemisphere_image_urls()

	return {
		'nasa_news' : nasa_news, # get the most recent entry only
		'jpl_featured_image' : jpl_featured_image,
		'mars_weather' : mars_weather,
		'mars_facts' : mars_facts,
		'hemisphere_image_urls' : hemisphere_image_urls
	}
	
def scrape_nasa():
	# Scrape NASA Mars News
	url_nasa = "https://mars.nasa.gov/news/"

	news_list = []

	try:
		# Retrieve page with WerbDriver, not request - complex page buildup
		browser = get_browser()
		browser.visit(url_nasa)

		# Create BeautifulSoup object; parse with 'html.parser'
		soup = bs(browser.html, 'html.parser')

		# Collect the latest News Title and Paragraph Text. 
		# Assign the text to variables for later reference.
		news_items = soup.find_all('div', class_='image_and_description_container')
		
		for item in news_items: 
			news = item.find('div', class_='list_text')
			if news:
				n_date = news.find('div', class_='list_date').text
				n_title = news.find('a').text
				n_teaser = news.find('div', class_='article_teaser_body').text
				#print(f"{n_date}\n{n_title}\n{n_teaser}\n")
				news_list.append({'n_date' : n_date, 'n_title': n_title, 'n_teaser' : n_teaser})
	except:
		print("Error during JPL scraping")
	finally:
		browser.quit()	
	
	return news_list
	

def scrape_jpl():
	# Scrape site
	url_jpl = "https://www.jpl.nasa.gov"
	url_jpl_mars = url_jpl + "/spaceimages/?search=&category=Mars"

	full_image_href = None
	try:
		browser = get_browser()
		browser.visit(url_jpl_mars)

		# Click on the first button : "FULL IMAGE"
		browser.click_link_by_id('full_image')

		# Check of the element presense and the delay is required due to asyc pages loading	
		browser.is_element_not_present_by_text('more info', wait_time=2)
		# Click on second button : "more info"
		browser.click_link_by_partial_text('more info')

		# Create BeautifulSoup object with 'html.parser'
		soup = bs(browser.html, 'html.parser')
		figure = soup.find('figure')
		full_image_href = url_jpl + figure.find('a')['href'].strip()

	except:
		print("Error during JPL scraping")
	finally:
		browser.quit()
	
	return full_image_href


def scrape_mars_weather():
	# Scrape site
	url_twit = "https://twitter.com/marswxreport?lang=en"

	try:
		browser = get_browser()
		browser.visit(url_twit)

		# Create BeautifulSoup object; parse with 'html.parser'
		soup = bs(browser.html, 'html.parser')

		# Get current weather
		weather_container = soup.find('div', class_='stream')
		weather_current = weather_container.find('p')
		mars_weather = weather_current.text.strip()
	except:
		print("Error during JPL scraping")
	finally:
		browser.quit()
	
	return mars_weather	
	
	
def scrape_mars_facts():
	try:
		# Scrape facts using pandas
		url_mars_facts = "https://space-facts.com/mars/"
		mars_facts_df = pd.read_html(url_mars_facts)[1] # data in second table
		mars_facts_df.columns = ['Parameter', 'Value']
	except:
		print("Error during JPL scraping")
		
	return mars_facts_df


def scrape_hemisphere_image_urls():
	# Scrape site
	url_usgs = "https://astrogeology.usgs.gov"
	url_usgs_mars = url_usgs + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

	hemisphere_image_urls = []

	try:
		browser = get_browser()
		browser.visit(url_usgs_mars)

		# Create BeautifulSoup object; parse with 'html.parser'
		soup = bs(browser.html, 'html.parser')

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
	except:
		print("Error during JPL scraping")
	finally:
		browser.quit()

	return hemisphere_image_urls


data_all = scrape_all()
print(data_all)


