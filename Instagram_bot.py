import time, os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
CHOSEN_ACCOUNT = os.environ["CHOSEN_ACCOUNT"]

class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        time.sleep(2)

    def login(self):
        self.driver.get('https://www.instagram.com/?flo=true')
        time.sleep(5)
        username_entry = self.driver.find_element(By.CSS_SELECTOR,'input[aria-label="Phone number, username or email address"]')
        password_entry = self.driver.find_element(By.CSS_SELECTOR,'input[aria-label="Password"]')

        time.sleep(5)
        username_entry.send_keys(USERNAME)
        password_entry.send_keys(PASSWORD,Keys.ENTER)
        time.sleep(5)

        popup = self.driver.find_element(By.XPATH,'//div[contains(text(), "Not now")]')
        popup.click()


    def find_followers(self):
        time.sleep(10)
        self.driver.get(f"https://www.instagram.com/[{CHOSEN_ACCOUNT}]/followers/")
        time.sleep(5)
        follower_count = self.driver.find_element(By.XPATH,'//span[contains(text()," followers")]')
        follower_count.click()

    def follow(self):
        time.sleep(10)
        follow_buttons = self.driver.find_elements(By.XPATH,'//*[text()="Follow"]')

        for button in follow_buttons[:5]:
            print(button)
            time.sleep(10)
            try:
                button.click()
            except NoSuchElementException:
                pass



insta_bot = InstaFollower()
insta_bot.login()
insta_bot.find_followers()
insta_bot.follow()
