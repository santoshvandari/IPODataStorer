import os

os.system("sudo -H python -m pip install --upgrade pip")
# os.system('pip install -r requirements.txt')
# psycopg2-binary
# Scrapy
# scrapy-playwright

print("Installing Dependencies")
os.system('sudo pip install psycopg2-binary')
os.system('sudo pip install Scrapy')
print("Installing Playwright and Scrapy-Playwright packages")
os.system('sudo pip install scrapy-playwright')
print("Installing Playwright")
os.system('sudo playwright install')
os.system('scrapy crawl ipo')