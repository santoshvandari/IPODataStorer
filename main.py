import datetime,psycopg2
import cloudscraper,random
import json


# Connecting to the Database
connectionString = "postgres://postgres.xirdbhvrdyarslorlufu:9XEq4EPhvJzDXfA7@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
try:
    connection = psycopg2.connect(connectionString)
    cursor = connection.cursor()
    print("Connected to PostgreSQL database successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)



# Getting the Data from the API
def get_api_data(api_url):
    try:
        # List of user agents to rotate
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]

        # Create a CloudScraper instance to bypass bot protection
        scraper = cloudscraper.create_scraper(
            delay=10,
            browser={
                'custom': 'ScraperBot/1.0',
            }
        )

        # Add headers to mimic a real browser request
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'keep-alive'
        }

        # Send a GET request to the URL with headers
        response = scraper.get(api_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the HTML content of the webpage
            return response.text
        else:
            # Print an error message if the request fails
            print(f"Failed to fetch URL: {api_url} . Status code: {response.status_code}")
            return None
    except Exception as e:
        # Print an error message if an exception occurs during the request
        print(f"An error occurred while fetching URL: {api_url}. Error: {str(e)}")
        return None
# Handeling the Right Share Data
def RightShare(data):
    for i in range(len(data)):
        closingdate=data[i]['closing_date']
        if closingdate:
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate >= today:
            # if True:
                openingdate=data[i]['opening_date']
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit=data[i]['units']
                companyname=data[i]['company_name']
                symbol=data[i]['symbol']
                issuetype='Right Share'
                issuefor = "General Public"
                issuemanager = data[i]['issue_manager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)

# Handeling the IPO Data
def IPOHandeling(data):
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["closing_date"]
        if data[i]['last_closing_date']:
            closingdate=data[i]['last_closing_date']
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate >= today:
            # if True:
                openingdate = data[i]["opening_date"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = data[i]["units"]
                companyname = data[i]["company_name"]
                symbol = data[i]["symbol"].split("(")[0]
                if not companyname:
                    companyname = symbol
                issuetype='IPO'
                # check the symbols contains ( or not 
                if data[i]["symbol"].__contains__("("):
                    issuefor = data[i]["symbol"].split("(")[1].split(")")[0]
                else:
                    issuefor="General Public"
                issuemanager = data[i]['issue_manager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)

# Haneling the FPO Data
def FPOHandeling(data):
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["closing_date"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate >= today:
            # if True:
                openingdate = data[i]["opening_date"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = data[i]["units"]
                companyname = data[i]["company_name"]
                symbol = data[i]["symbol"]
                issuetype='FPO'
                issuefor = "General Public"
                issuemanager = data[i]['issue_manager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)


# Hanelig the Auction Share Data
def AuctionHandeling(data):
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["close_date"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate >= today:
            # if True:
                openingdate = data[i]["open_date"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = (data[i]["units"]).split(".")[0]
                companyname = data[i]["company"]
                symbol = data[i]["symbol"]
                issuetype='Aution Share'
                issuefor = "General Public"
                issuemanager = data[i]['issue_manager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)

# Handeling the Mutual Fund Data
def MutualFundHandeling(data):
    for i in range(len(data)):
        closingdate = data[i]["closing_date"]
        if data[i]['last_closing_date']:
            closingdate=data[i]['last_closing_date']
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate >= today:
            # if True:
                openingdate = data[i]["opening_date"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = (data[i]["units"]).split(".")[0]
                companyname = data[i]["company_name"]
                symbol = data[i]["symbol"]
                issuetype='Mutual Fund'
                issuefor = "General Public"
                issuemanager = data[i]['issue_manager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)



def FilterData(response):
    # Filter the data
    data = response
    RightShare(data["rights"])
    IPOHandeling(data["ipo"])
    FPOHandeling(data["fpo"])
    AuctionHandeling(data["auction"])
    MutualFundHandeling(data["mutual_fund"])

def WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager):
    if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
        # Storing in the Database
        query=f"INSERT INTO ipodetails(openingdate,closingdate,totalissueunit,companyname,symbol,issuetype,issuefor,issuemanager) VALUES('{openingdate}','{closingdate}',{totalissueunit},'{companyname}','{symbol}','{issuetype}','{issuefor}','{issuemanager}');"
        print(query)
        cursor.execute(query)
    print("Data Written to Database")


if __name__ == "__main__":
    today = datetime.datetime.now().date()
    if today.strftime("%A") == "Saturday":
        print("Today is Saturday")
        exit(0)
    else:
        api_url = "https://www.nepsealpha.com/api/smx9841/investment_calander"
        api_data = get_api_data(api_url)
        if api_data:
            cursor.execute('truncate ipodetails;')
            FilterData(json.loads(api_data))
        else:
            print("Error fetching API data.")
    connection.commit()
    connection.close()