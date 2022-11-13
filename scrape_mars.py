# get dependencies

from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests 
import datetime as dt

# scarape all function
def scrape_all():
    # splinter setup

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    # the aim is to return  a json that has all the needed data, so that we can load into mongodb

    # get the information from the news page
    news_title, news_paragraph = scrape_news(browser)

    # build a dictionary using the information from the scrapes
    marsData = {
        "newsTitle": news_title,
        "newsparagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": hemispheres(browser),
        "lastUpdted": dt.datetime.now()
    }

    # stop the webdriver
    browser.quit()

    # display output
    return marsData
# scrape through the featured image page
def scrape_feature_img(browser):
    # visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # find and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()
    
    # parse the resulting html with soup
    html = browser.html
    image_soup = soup(html, 'html.parser')


    img_url_rel = image_soup.find('img', class_='fancybox-image').get('src')

    # use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    # return the image URL
    return img_url

# scrape through the facts page
def scrape_facts_page(browser):
    # visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    

# scrape the mars news page
def scrape_news(browser):
    # go to Mars Nasa news website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    # optional delay to load the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # conver browser into a soup object

    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    # grab the title
    news_title = slide_elem.find('div', class_= 'content_title').get_text()

    # grab the paragraph for headlines
    news_p = slide_elem.find('div', class_= 'article_teaser_body').get_text()

    # return the news title and the paragraph
    return news_title, news_p



#scrape through the featured image page

# scrape through the facts page
def scrape_facts_page(browser):
    # visit url
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    # parse the resulting html with soup
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    # find the facts location
    factsLocation = fact_soup.find('div', class_= "diagram mt-4")
    factTable = factsLocation.find('table') # grab html code for the facts table

    # create an empty string
    facts = ""

   

    # add the text to the empty string then return
    facts += str(factTable)

    return facts



# scrape through the hemishperes pages
def hemispheres(browser):
    # base url
    url = "https://marshemispheres.com/"
    browser.visit(url) 

    # create a list to hold the images and titles,
    hemisphere_image_urls = []

    # set up a loop
    for i in range(4):
        # loop through each of the pages
        # create hemisphere dictionary
          
        hemisphereInfo = {}
    
        # we have to find the elements on each loop to avoid a state element exception
        browser.find_by_css('a.product-item img')[i].click()
     
    
        # Next, we find the sample image anchor tag and extract the href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo['img_url'] = sample['href']
    
        # get the hemisphere title
        hemisphereInfo['title']= browser.find_by_css('h2.title').text
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
        # Finaly, we navigate backwords
        browser.back() 
    
    return hemisphere_image_urls
     

if __name__ == "__main__":
    print(scrape_all())
 
