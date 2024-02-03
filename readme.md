# Instagram Scraper

This project contains scripts to scrape Instagram data.

## Files

### [specific_user_scraper.py](specific_user_scraper.py)
This script is used to scrape Instagram data for a specific user. It uses the `InstaStoryScraper` class to scrape the user's Instagram stories.

Usage:
```bash
python specific_user_scraper.py <username>
```
Replace <username> with the Instagram username you want to scrape.

### [followed_users_scraper.py](followed_users_scraper.py)
This script is used to scrape Instagram data for users followed by a specific account. It uses the FollowedUsersStoryScraper class to scrape the Instagram stories of the followed users.

Usage:
```bash
python followed_users_scraper.py
```

## Dependencies
This project uses Selenium WebDriver for web scraping. Make sure to install it in your Python environment:

<!-- License
This project is licensed under the terms of the MIT license. -->