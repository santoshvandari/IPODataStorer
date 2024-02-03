import os

os.system('pip install -r requirements.txt')
os.system('playwright install')
os.system('scrapy crawl ipo')