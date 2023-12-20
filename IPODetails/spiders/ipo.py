# Command: scrapy crawl ipo and store in the postgresql database of the supabase   
import scrapy, psycopg2, datetime
from scrapy_playwright.page import PageMethod
from pathlib import Path

# Connecting to the Database
connectionString = "postgresql://postgres:rnR0uiDqNVWiBL1C@db.xirdbhvrdyarslorlufu.supabase.co:5432/postgres"
try:
    connection = psycopg2.connect(connectionString)
    cursor = connection.cursor()
    cursor.execute('truncate ipodetails;')
    print("Connected to PostgreSQL database successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

# Defining the Spider
class PwspiderSpider(scrapy.Spider):
    name = 'ipo'
    allowed_domains = ['sarallagani.com']
    start_urls = ['https://sarallagani.com/investment-opportunity']
    def start_requests(self):
        yield scrapy.Request('https://sarallagani.com/investment-opportunity',
                            meta=dict(
                                playwright=True,
                                playwright_include_page=True,
                                playwright_page_methods=[
                                    # This where we can implement scrolling if we want
                                    PageMethod('wait_for_selector', 'table tbody.ant-table-tbody'),
                                ]
                            )
                            )
    async def parse(self, response):
        # Writing all the output in html file
        # Path("output.html").write_text(await response.page.content())
        tabledata= response.css('table tbody.ant-table-tbody tr')
        for data in tabledata:
            name = (data.css('td:nth-child(1)::text').get()).split('[')[0]
            totalunit = int(data.css('td:nth-child(4)::text').get())
            openingdatestr = data.css('td:nth-child(5)::text').get()
            openingdate= datetime.datetime.strptime(openingdatestr, '%Y-%m-%d').date()
            closingdatestr = data.css('td:nth-child(6)::text').get()
            closingdate= datetime.datetime.strptime(closingdatestr, '%Y-%m-%d').date()
            # if(closingdate>=datetime.date.today()):
            if(True):
                
                # Storing in the Database
                query=f"INSERT INTO ipodetails VALUES('{name}',{totalunit},'{openingdate}','{closingdate}');"
                print(query)
                cursor.execute(query)
        # Commiting the Every Query to the Database
        connection.commit()

                






# password of Database: rnR0uiDqNVWiBL1C