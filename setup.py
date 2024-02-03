import os

os.system("python -m pip install --upgrade pip")
os.system('pip install -r requirements.txt')
print("Installing Playwright and Scrapy-Playwright packages")
os.system('pip install scrapy-playwright')
print("Installing Playwright")
os.system('playwright install')
os.system('scrapy crawl ipo')