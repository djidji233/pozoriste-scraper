# pozoriste-scraper

Scrapes websites for 2 theater shows (others were bought and watched with the help of this scraper).
Checks for new dates (at the end of the month) and sends an email with the dates it found so I can buy the tickets before they sell out.

Technologies used: Python with BeautifulSoup

Deployment: Railway (with built-in Cron scheduler for 9 AM)

Plans:
- create a landing page to select the shows from a dropdown and leave your email
- import that data to a google sheet and read from it and send the emails automatically based on that data
