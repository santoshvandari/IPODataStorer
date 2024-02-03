import os

# os.system('pip install -r requirements.txt')
os.system("python -m pip install --upgrade pip")
print("Installing Playwright and Scrapy-Playwright packages")
os.system('pip install scrapy-playwright')
print("Installing Playwright")
os.system('playwright install')
os.system('scrapy crawl ipo')