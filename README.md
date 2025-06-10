# pozoriste-scraper

Scrapes websites for 2 theater shows (others were bought and watched with the help of this scraper).
Checks for new dates (at the end of the month) and sends an email with the dates it found so I can buy the tickets before they sell out.

Technologies used: Python with BeautifulSoup

Deployment: Railway (with built-in Cron scheduler)

Plans:
- create a micro-SaaS out of this (probably as a separate repo)
- create a landing page to select the shows from a dropdown and leave your email
- save data to a database and send the emails automatically to all recepients

Since it was already deployed, it was convenient to add 2 more scrapers for Beogradska Arena and Sava Centar to know if there will be traffic jams and problems with parking in my neighbourhood.
