# Dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import requests

# Set path to chromedriver
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_info = {}


    # Scrape latest Mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")

    sidebar = soup.find("ul", class_="item_list")
    categories = sidebar.find_all("li")

    for category in categories[0]:
        div = category.find("div", class_="list_text")
        div2 = div.find("div", class_="content_title")
        target = div2.find("a")
        mars_info["news_title"] = target.text
        mars_info["news_p"] = div.find("div", class_="article_teaser_body").text


    # Scrape Mars image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, "html.parser")

    img_sidebar = soup.find("ul", class_="articles")
    img_categories = img_sidebar.find("li")
    target = img_categories.find("a")["data-fancybox-href"]
    mars_info["featured_image_url"] = "https://www.jpl.nasa.gov" + target
    

    # Scrape latest Mars weather report
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(tweet_url)
    
    tweet_soup = bs(response.text, "lxml")
    
    tweet_find = tweet_soup.find("div", class_="js-tweet-text-container")
    mars_info["mars_weather"] = tweet_find.find("p", class_="tweet-text").text


    # Scrape Mars facts table
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    
    df = tables[0]
    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    html_table = df.to_html()
    html_table.replace("\n", "")
    mars_info["html_table"] = html_table
    

    # Scrape Mars hemisphere content
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    time.sleep(1)
    
    hemisphere_image_urls = []
    
    html = browser.html
    soup = bs(html, "html.parser")

    links = soup.find_all("a", class_="itemLink")
    
    for i in links[1::2]:
        hemisphere = {}
        url = "https://astrogeology.usgs.gov" + i["href"]
        browser.visit(url)
        time.sleep(0.5)
        
        html = browser.html
        soup = bs(html, 'html.parser')

        img_url = soup.find_all("a", class_="itemLink")
        hemisphere["title"] = browser.find_by_css("h2.title").text
        sample = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]

        hemisphere_image_urls.append(hemisphere)
     
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls
    

    return mars_info