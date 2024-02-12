import requests,datetime,psycopg2

# Connecting to the Database
# connectionString = "postgres://postgres.xirdbhvrdyarslorlufu:9XEq4EPhvJzDXfA7@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
# try:
#     connection = psycopg2.connect(connectionString)
#     cursor = connection.cursor()
#     cursor.execute('truncate ipodetails;')
#     print("Connected to PostgreSQL database successfully!")
# except Exception as e:
#     print(f"Error connecting to database: {e}")
#     exit(1)

# Getting the Data from the API
def get_api_data(api_url):
    with open("data.json","r") as f:
        print(f.read())

    try:
        pass
        # response = requests.get(api_url)
        # if response.status_code == 200:
        #     if response.json():            
        #         data=response.json()
        #         FilterData(data)
        #     else:
        #         print("Error: API Response is NULL")
        #         exit(1)
        # else:
            
        #     print(f"Error: {response.status_code} - {response.text}")
        #     exit(1)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)
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
                issuetype='FPO'
                issuefor = data[i]["symbol"].split("(")[1].split(")")[0]
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
    pass
    # Filter the data
    # data = response
    # RightShare(data["rights"])
    # IPOHandeling(data["ipo"])
    # FPOHandeling(data["fpo"])
    # AuctionHandeling(data["auction"])
    # MutualFundHandeling(data["mutual_fund"])

def WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager):
    if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
        # Storing in the Database
        # query=f"INSERT INTO ipodetails(openingdate,closingdate,totalissueunit,companyname,symbol,issuetype,issuefor,issuemanager) VALUES('{openingdate}','{closingdate}',{totalissueunit},'{companyname}','{symbol}','{issuetype}','{issuefor}','{issuemanager}');"
        # print(query)
        print(f"Opening Date : {openingdate}\nClosing Date : {closingdate}\nTotal IssueUnit : {totalissueunit}\nCompany Name : {companyname}\nSymbol : {symbol}\nIssue Type : {issuetype}\nIssue For : {issuefor}\n Issue Manager : {issuemanager}")
        # cursor.execute(query)
    print("Data Written to Database")


if __name__ == "__main__":
    api_url="https://www.nepsealpha.com/api/smx9841/investment_calander"
    # get_api_data(api_url)
    # connection.commit()
    pass
    get_api_data(api_url)