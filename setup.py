import os

os.system("python -m pip install --upgrade pip")
# os.system('pip install -r requirements.txt')
# psycopg2-binary
# Scrapy
# scrapy-playwright

print("Installing Dependencies")
os.system('pip install psycopg2-binary')
os.system('pip install Scrapy')
print("Installing Playwright and Scrapy-Playwright packages")
os.system('pip install scrapy-playwright')
print("Installing Playwright")
os.system('playwright install')
# os.system('scrapy crawl ipo')