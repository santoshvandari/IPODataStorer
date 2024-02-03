import os

os.system('pip install -r requirements.txt')
print("Installing Playwright and Scrapy-Playwright")
os.system('pip install scrapy-playwright')
os.system('playwright install')
# os.system('scrapy crawl ipo')