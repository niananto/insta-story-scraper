
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from termcolor import colored
import urllib.request
import os
import time
import uuid
from dotenv import load_dotenv
import sys


class SpecificUserStoryScraper:
    """
    A class for scraping stories, and downloading the result.
    ...

    Attributes
    ----------
    :param username: username for the account to scrap.

    Methods
    -------
    download(url, is_video, dir): Download a content given its url.
    download_all(): Download all scraped content.
    scraper(): Scrap stories from Instagram account.

    """

    def __init__(self, username, chrome_driver_path):
        """
        Constructs all the necessary attributes for the SpecificUserStoryScraper object.
        :param username: username for the account to scrap.
        :param chrome_driver_path: path to the chrome driver.
        """
        load_dotenv()
        self.usr = os.getenv("USR")
        self.pswd = os.getenv("PSWD")
        # print(self.usr, self.pswd)
        self.username = username
        self.project_direc = '/'.join(os.getcwd().split('/')[:-1])
        self.login_page = "https://www.instagram.com/accounts/login/"
        self.story_link = "https://www.instagram.com/stories/{}/".format(username)
        self.chrome_driver_path = chrome_driver_path

    @staticmethod
    def download(url, is_video, dir):
        """
        Download a content given its URL.
        :param url: Content URL.
        :param is_video: Whether it's a video or image.
        :param dir: Path to directory.
        :return:
        """
        filename = '.'.join((uuid.uuid4().hex, 'mp4')) if is_video else '.'.join((uuid.uuid4().hex, 'jpg'))
        try:
            print("Downloading starts...\n")
            urllib.request.urlretrieve(url, os.path.join(dir, filename))
            print("Downloading completed ..!! \n")
        except Exception as e:
            print(e)

    def download_all(self):
        """
        Download all scraped content.
        :return:
        """
        file_path = os.path.join(self.project_direc, "collected_data/pickles/stories_{}.pkl".format(self.username))
        if not os.path.exists(file_path):
            print(colored("\n[ERROR]: Can't download, stories were not scraped. \n", "red"))
        else:
            dir = os.path.join(self.project_direc, "collected_data/"+self.username)
            if not os.path.exists(dir): os.makedirs(dir)
            df = pd.read_pickle(file_path)
            for i, row in df.iterrows():
                SpecificUserStoryScraper.download(row["Content URL"], row["is_video"], dir)

    def scraper(self):
        """
        Scraping stories.
        :return:
        """
        # Specify Chrome driver options
        # service = Service("chromedriver_win64\chromedriver.exe")
        service = Service(self.chrome_driver_path)
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = webdriver.Chrome(service=service, options=options)
            
        driver.get(self.login_page)
        time.sleep(4)

        # # Accept the website cookies
        # driver.find_element(By.XPATH, "/html/body/div[4]/div/div/button[1]").click()
        # time.sleep(3)

        # Login with a random account since we can't scrap stories without being logged
        driver.find_element(By.NAME, "username").send_keys(self.usr)
        driver.find_element(By.NAME, "password").send_keys(self.pswd)

        # Check that we had access to the account, otherwise keep retrying
        driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(5)
        print(colored("\n[SUCCESS]: Logged into the website. \n", "green"))

        # Get access to the story link
        driver.get(self.story_link)
        time.sleep(1)

        # Check if there are any stories for the last 24h, if so start scraping all stories
        if driver.current_url != self.story_link:
            print(colored("\n[ERROR]: No stories are available for the last 24h. \n", "red"))
        else:
            rows = []
            print(colored("\n[SUCCESS]: Got into the story link. \n", "green"))
            buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
            for button in buttons:
                if button.get_attribute('innerHTML') == 'View story':
                    button.click()
                    break 
                
            while driver.current_url != "https://www.instagram.com/":
                # Collect the link to the video content of the story if it exists, otherwise take the image link
                is_video = False
                try:
                    content_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/section/div[1]/div/div/div[1]/div[2]/div[1]/div/img')
                    content_link = content_element.get_attribute('src')
                except NoSuchElementException:
                    is_video = True
                    probable_elements = driver.find_elements(By.CSS_SELECTOR, 'video')
                    for element in probable_elements:
                        print(element.get_attribute('innerHTML'))
                    content_link = probable_elements[0].get_attribute('src')

                print(colored(f"\n[SUCCESS]: Got the content link:\n\t{content_link}. \n", "green"))

                # Get the link of the story
                insta_link = driver.current_url

                # Get the date of the story
                date = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/section/div[1]/div/div/div[1]/div[1]/div[2]/div[1]/div/div/div/div/span/time') \
                    .get_attribute("datetime")

                # Append all collected information into a row
                rows.append(
                    {
                        'Instagram URL': insta_link,
                        'Content URL': content_link,
                        'Date': date,
                        'is_video': is_video
                    }
                )

                # Click on the next button
                # Click on the next button
                try:
                    buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                    for button in buttons:
                        if button.get_attribute('innerHTML').find('Next') != -1:
                            button.click()
                            break
                except:
                    break

                time.sleep(1)

            # Save scrapped data into a dataframe
            df = pd.DataFrame(rows)
            tmp = os.path.join(self.project_direc, "collected_data", "pickles")
            if not os.path.exists(tmp): os.makedirs(tmp)
            df.to_pickle(os.path.join(tmp, "stories_{}.pkl".format(self.username)))
            driver.quit()
            print(colored("\n[SUCCESS]: Scrapped all stories for the last 24h. \n", "green"))

def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input(colored("\n[INFO]: Please type the username you want to scrap stories from: ", "yellow"))
        
    if len(sys.argv) > 2:
        chrome_driver_path = sys.argv[2]
    else:
        chrome_driver_path = os.path.join(os.getcwd(), "chromedriver_win64", "chromedriver.exe")
        
    scrp = SpecificUserStoryScraper(username, chrome_driver_path)
    scrp.scraper()
    scrp.download_all()

# main()