# Instagram Scraper

This project contains scripts to scrape Instagram data.

## Files

### [specific_user_scraper.py](specific_user_scraper.py)
This script is used to scrape Instagram data for a specific user. It uses the `InstaStoryScraper` class to scrape the user's Instagram stories.

Usage:  
uncomment the last line and run this replacing the `<username>` with the Instagram username you want to scrape.
```bash
python specific_user_scraper.py <username>
```

### [followed_users_scraper.py](followed_users_scraper.py)
This script is used to scrape Instagram data for users followed by a specific account. It uses the FollowedUsersStoryScraper class to scrape the Instagram stories of the followed users.

Usage:  
uncomment the last line and run this-
```bash
python followed_users_scraper.py
```

## IMPORT
```python
from specific_user_scraper import SpecificUserStoryScraper


```
```python
from followed_users_scraper import FollowedUsersStoryScraper
```

## Dependencies
This project uses Selenium WebDriver for web scraping. Make sure to install it in your Python environment:

<!-- License
This project is licensed under the terms of the MIT license. -->