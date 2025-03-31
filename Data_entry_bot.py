import time, os, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()

header = {
    "User-Agent":os.environ["USER_AGENT"],
    "Accept-Language":os.environ["LANGUAGE"],
}


#Scraping data from website
response = requests.get(os.environ["DEMO_WEBSITE_LINK"], headers=header)
data = response.text
soup = BeautifulSoup(data,"html.parser")

#Finding all the links
all_link_elements = soup.select('.StyledPropertyCardDataWrapper a')
all_links = [link['href'] for link in all_link_elements]
print(f"There are {len(all_links)} links to individual listings in total: \n")

#Finding all the addresses and cleaning the data
all_address_element = soup.select('.StyledPropertyCardDataWrapper address')
all_addresses = [address.get_text().replace("|"," ").strip() for address in all_address_element]
print(f"\n After having been cleaned up, the {len(all_addresses)} addresses now look like this: \n")

#Finding all the prices and cleaning the data
all_price_elements = soup.select('.PropertyCardWrapper span')
all_prices = [price.get_text().replace("/mo","").split("+")[0] for price in all_price_elements if "$" in price.text]


#Keeps chrome open on screen
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_link_elements)):
    #Gets the bot to opn the sheet
    driver.get(os.environ['GOOGLE_SHEET_LINK'])
    time.sleep(2)

    #Find the needed elements
    address_input = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = button = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    #Sending data to the found elements
    address_input.send_keys(all_addresses[n])
    price_input.send_keys(all_prices[n])
    link_input.send_keys(all_links[n])
    submit.click()#Click submit button to submit the form
