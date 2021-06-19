# Web Scrapinh Homework Mission to Mars

# Dependencies

from bs4 import BeautifulSoup as bs
import os
import requests
import pymongo
import pandas as pd
from urllib.parse import urljoin
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA MARS NEWS

    # URL opened with Chrome
    news_url = 'https://redplanetscience.com'
    browser.visit(news_url)

    # Scrape Site into Soup
    html = browser.html
    soup = bs(html,'html.parser')

    # News Title
    results = soup.find_all('div', class_='list_text')
    for result in results:
        news_title = result.find('div', class_='content_title').text
        news_paragraph = result.find('div', class_='article_teaser_body').text

    # JPL MARS SPACE IMAGES

    # Featured Space Image Site
    url_image = 'https://spaceimages-mars.com'
    browser.visit(url_image)

    # Scrape Site into Soup
    html_image = browser.html
    soup = bs(browser.html, 'html.parser')

    # Find Image
    featured_image = soup.find_all('img', class_='headerimage fade-in')

    # Save complete url string for this image
    featured_image_url = f"{url_image}/{featured_image[0]['src']}"

    # MARS FACTS

    # Mars Facts
    url_facts = "https://galaxyfacts-mars.com/"

    # Use Pandas to Convert the data to HTML table string

    facts_table = pd.read_html(url_facts)


    # Facts about the planet: Diameter, Mass...
    mars_df_facts = facts_table[0]
    mars_df_facts.columns=['Mars-Earth Comparison', 'Mars', 'Earth']
    mars_df_facts.drop(0, inplace=True)
    html_content = [mars_df_facts.columns.values.tolist()] + mars_df_facts.values.tolist()


    # MARS HEMISPHERES

    # Astreology Site
    url = 'https://marshemispheres.com'
    browser.visit(url)

    # Soup for the Site
    html = browser.html
    soup = bs(html, 'html.parser')

    # Hemispheres
    hemisphere_items = soup.find_all('div', class_='item')

    # List Dictionary Loop

    url = 'https://marshemispheres.com/'
    hemisphere_images = []

    for item in hemisphere_items:
        hemisphere_dict = {}
        item_link = item.find('a', class_='itemLink')['href']
        item_title = item.find('h3').text
        browser.visit(url+item_link)
        html = browser.html
        soup = bs(html, 'html.parser')
        item_downloads = soup.find('div', class_='downloads')
        item_img = item_downloads.ul.li.find('a')['href']
        hemisphere_dict["title"] = item_title
        hemisphere_dict["img_url"] = urljoin(url,item_img)
        hemisphere_images.append(hemisphere_dict)

    # MARS DATA

    mars_data = {}
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph
    mars_data["featured_image"] = featured_image_url
    mars_data["mars_facts"] = html_content
    mars_data["mars_hemispheres"] = hemisphere_images

    # Broswer Quit
    browser.quit()

    return mars_data









