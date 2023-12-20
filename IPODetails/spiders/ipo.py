import scrapy, psycopg2, datetime
from scrapy_playwright.page import PageMethod
connectionString = "postgresql://postgres:rnR0uiDqNVWiBL1C@db.xirdbhvrdyarslorlufu.supabase.co:5432/postgres"
try:
    connection = psycopg2.connect(connectionString)
    cursor = connection.cursor()
    cursor.execute('truncate ipoinfo;')
    print("Connected to PostgreSQL database successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)
class PwspiderSpider(scrapy.Spider):
    name = 'ipo'
    allowed_domains = ['nepsebajar.com']
    start_urls = ['https://www.nepsebajar.com/ipo-pipelinewewe']
    def start_requests(self):
        yield scrapy.Request('https://www.nepsebajar.com/ipo-pipelinewewe',
                            meta=dict(
                                playwright=True,
                                playwright_include_page=True,
                                playwright_page_methods=[
                                    # This where we can implement scrolling if we want
                                    PageMethod('wait_for_selector', 'table.display.table-bordered.mb-5 tbody tr'),
                                ]
                            )
                            )
    async def parse(self, response):
        tabledata= response.css('table#example tbody tr')
        date = datetime.date.today()
        for data in tabledata:
            companyname = data.css('td:nth-child(1) a::text').get()
            symbol = data.css('td:nth-child(2) a::text').get()
            totalissueunit = int(data.css('td:nth-child(3)::text').get())
            issuetypeinfo=(data.css('td:nth-child(4)::text').get())
            if issuetypeinfo.find('-')!=-1:
                issuetypeinfo=(data.css('td:nth-child(4)::text').get()).split('-')[1]

            if issuetypeinfo.find('For')!=-1:
                issuetype = issuetypeinfo.split('For')[1]
            else:
                issuetype = issuetypeinfo
            issuemanager=data.css('td:nth-child(5)::text').get()
            openingdate = (data.css('td:nth-child(6)::text').get()).replace('/','-')
            closingdate = (data.css('td:nth-child(7)::text').get()).replace('/','-')
            if(closingdate>=date):
                query=f"INSERT INTO ipoinfo VALUES('{companyname}','{symbol}',{totalissueunit},'{issuetype}','{issuemanager}','{openingdate}','{closingdate}');"
                print(query)
                cursor.execute(query)
        connection.commit()