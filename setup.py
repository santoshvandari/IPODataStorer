import os

os.system('pip install -r requirements.txt')
os.system('pip install scrapy-playwright')
os.system('playwright install')
os.system('scrapy crawl ipo')