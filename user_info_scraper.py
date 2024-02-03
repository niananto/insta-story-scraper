from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from termcolor import colored
import os
import time
from dotenv import load_dotenv
import sys


class UserInfoScraper:
    """
    A class for scraping information of a certain user.
    ...

    Attributes
    ----------
    :param username: username for the account to scrap.

    Methods
    -------
    scraper(): Scrap information of the user.

    """

    def __init__(self, username):
        """
        Constructs all the necessary attributes for the SpecificUserStoryScraper object.
        :param username: username for the account to scrap.
        """
        load_dotenv()
        self.usr = os.getenv("USR")
        self.pswd = os.getenv("PSWD")
        # print(self.usr, self.pswd)
        self.username = username
        self.project_direc = '/'.join(os.getcwd().split('/')[:-1])
        self.login_page = "https://www.instagram.com/accounts/login/"
        self.story_link = "https://www.instagram.com/stories/{}/".format(username)
        
    def scraper(self):
        """
        Scraping information.
        :return:
        """
        
        service = Service("chromedriver_win64\chromedriver.exe")
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        driver = webdriver.Chrome(service=service, options=options)
            
        from dotenv import load_dotenv
        load_dotenv()
        usr = os.getenv("USR")
        pswd = os.getenv("PSWD")
        login_page = "https://www.instagram.com/accounts/login/"
        driver.get(login_page)
        time.sleep(4)

        # Login with a random account since we can't scrap stories without being logged
        driver.find_element(By.NAME, "username").send_keys(usr)
        driver.find_element(By.NAME, "password").send_keys(pswd)

        # Click the login button
        driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        print(colored("\n[SUCCESS]: Logged into the website. \n", "green"))
        time.sleep(5)
                
        # scrape information of the user
        user_link = f'https://www.instagram.com/{self.username}/'
        driver.get(user_link)
        time.sleep(10)
        dir = os.path.join("collected_data", "info")
        if not os.path.exists(dir): os.makedirs(dir)
        f = open(os.path.join(dir, f"{self.username}_info.txt"), "w")

        num_posts = driver.find_element(By.XPATH, \
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]').text
        num_followers = driver.find_element(By.XPATH, \
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]').text
        num_following = driver.find_element(By.XPATH, \
            '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]').text
        f.write('Number of posts: ' + num_posts + "\n")
        f.write('Number of followers: ' + num_followers + "\n")
        f.write('Number of following: ' + num_following + "\n\n")
          
        try:  
            bio = driver.find_element(By.XPATH, \
                '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1').text
            f.write(f'Bio: {bio}\n\n')
        except:
            f.write("No bio\n\n")

        try:
            threads_username = driver.find_element(By.XPATH, \
                '//*[@id="mount_0_0_Pa"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div[2]/a/span/span').text
            f.write('Threads username: ' + threads_username + "\n")
        except NoSuchElementException:
            f.write("No threads username\n")
            
        try:
            ext_link = driver.find_element(By.XPATH, '//*[@id="mount_0_0_Pa"]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div[3]/a/span/span').text
            f.write('External link: ' + ext_link + "\n")
        except NoSuchElementException:
            f.write("No external link\n")

        f.close()

def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter the username of the account: ")
    scraper = UserInfoScraper(username)
    scraper.scraper()
    
# main()