import scrapy
import psycopg2
import datetime
# from scrapy_playwright.page import PageMethod

# connectionString = "postgres://postgres.xirdbhvrdyarslorlufu:9XEq4EPhvJzDXfA7@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
class PwspiderSpider(scrapy.Spider):
    name = 'ipo'
    allowed_domains = ['nepsebajar.com']
    start_urls = ['https://www.nepsebajar.com/ipo-pipelinewewe']

    def __init__(self, *args, **kwargs):
        super(PwspiderSpider, self).__init__(*args, **kwargs)
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                "postgres://postgres.xirdbhvrdyarslorlufu:9XEq4EPhvJzDXfA7@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute('DELETE FROM ipoinfodetails;')
            print("Connected to PostgreSQL database successfully!")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.close_spider()


    def start_requests(self):
        yield scrapy.Request(
            'https://www.nepsebajar.com/ipo-pipelinewewe', callback=self.parse
        )

    async def parse(self, response):
        date = datetime.date.today()
        table_data = response.css('table#example tbody tr')

        for data in table_data:
            company_name = (data.css('td:nth-child(1) a::text').get()).strip()
            symbol = (data.css('td:nth-child(2) a::text').get()).strip()
            total_issue_unit = int(data.css('td:nth-child(3)::text').get())
            issue_type_info = data.css('td:nth-child(4)::text').get().strip()
            if '-' in issue_type_info:
                issue_type_info = data.css('td:nth-child(4)::text').get().split('-')[1].strip()
            if 'For' in issue_type_info:
                issue_type = issue_type_info.split('For')[1].strip()
            else:
                issue_type = issue_type_info

            issue_manager = (data.css('td:nth-child(5)::text').get()).strip()
            opening_date_str = data.css('td:nth-child(6)::text').get().replace('/', '-')
            opening_date = datetime.datetime.strptime(opening_date_str, '%Y-%m-%d').date()
            closing_date_str = data.css('td:nth-child(7)::text').get().replace('/', '-')
            closing_date = datetime.datetime.strptime(closing_date_str, '%Y-%m-%d').date()

            # Check if all fields are not empty
            if all([company_name, symbol, total_issue_unit, issue_type, issue_manager, opening_date, closing_date]):
                if closing_date >= date:
                # if True:
                    query = (
                        f"INSERT INTO ipoinfodetails VALUES "
                        f"('{company_name}','{symbol}',{total_issue_unit},'{issue_type}',"
                        f"'{issue_manager}','{opening_date}','{closing_date}');"
                    )
                    print(query)
                    self.cursor.execute(query)
        self.connection.commit()
        print("Data Writed Successfully!")
        if self.connection:
            self.connection.close()
            print("Closed PostgreSQL connection.")