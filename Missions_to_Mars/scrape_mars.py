# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
  
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_url = "https://redplanetscience.com/"

    browser.visit(news_url)

    html = browser.html

   
    news_soup = BeautifulSoup(html, 'html.parser')

    # MARS NEWS

    news_title = news_soup.find_all('div', class_="content_title")[0].text
    news_p = news_soup.find_all('div',class_='article_teaser_body')[0].text

    # MARS IMAGE

    jpl_mars_image_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_mars_image_url)
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    image_path = image_soup.find_all('div',class_='header')

    image_string = image_path[0].find('img', class_='headerimage')['src']
    
    image_url = f'{jpl_mars_image_url}{image_string}'

    # MARS FACTS
   
    facts_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(facts_url)
    
    mars_facts_df = tables[1]
    mars_facts_df.columns=['Measurement','Value']
  
    mars_html_table = mars_facts_df.to_html(index=False, justify='center')
    
    mars_html_table.replace('\n','')

    # MARS HEMISPHERES 
  
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemisphere_soup = BeautifulSoup(hemispheres_html, 'html.parser')

    all_hemisphere_list_dicts = []

    hemisphere_results = hemisphere_soup.find('div', class_="collapsible results")

    each_hemisphere = hemisphere_results.find_all('div', class_="item")

    for hemisphere in each_hemisphere:
 
        title = hemisphere.find('h3').text
     
        hemisphere = hemisphere.find('a', class_="itemLink product-item")['href']
        
        browser.visit(f'{hemispheres_url}{hemisphere}')
        
        image_html = browser.html
        img_soup = BeautifulSoup(image_html, 'html.parser')
        
        image = img_soup.find('div', class_='downloads')
   
        img_url = image.find('li').a['href']
        
        img_url_full = f'{hemispheres_url}{img_url}'
        
        hemisphere_dict = {"title":title,
                        "img_url":img_url_full}
        
        all_hemisphere_list_dicts.append(hemisphere_dict)

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": all_hemisphere_list_dicts
    }

    return mars_dict