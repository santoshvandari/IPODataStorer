# Using Saral lagani API 
import requests,datetime,psycopg2

# Connecting to the Database
connectionString = "postgres://postgres.xirdbhvrdyarslorlufu:9XEq4EPhvJzDXfA7@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
try:
    connection = psycopg2.connect(connectionString)
    cursor = connection.cursor()
    cursor.execute('truncate ipodetails;')
    print("Connected to PostgreSQL database successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

# Getting the Data from the API
def get_api_data(api_url):
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'sarallagani.xyz',
    'Origin': 'https://sarallagani.com',
    'Permission': '2021D@T@f@RSt6&%2-D@T@',
    }
    try:
        response = requests.get(api_url,headers=headers)
        if response.status_code == 200:
            data=(response.json())["data"]
            if data:     
                # print(data)       
                FilterData(data)
            else:
                print("Error: API Response is NULL")
                exit(1)
        else:
            
            print(f"Error: {response.status_code} - {response.text}")
            exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
# Handeling the Right Share Data
def RightShare(data):
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["closeDate"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate >= today:
                openingdate = data[i]["openDate"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = data[i]["unit"]
                companyname=data[i]["company_name"]
                issuefor = "General Public" 
                symbol = data[i]["symbol"]
                issuetype='Right Share'
                issuemanager = data[i]['issueManager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    pass
                    # print(f"Closig Date : {closingdate}\nOpening Date : {openingdate}\nTotal Issue Unit : {totalissueunit}\nCompany Name : {companyname}\nSymbol : {symbol}\nIssue Type : {issuetype}\nIssue For : {issuefor}\nIssue Manager : {issuemanager}")
                    # WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)
                    # pass

# Handeling the IPO Data
def IPOHandeling(data):
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["closeDate"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate >= today:
                openingdate = data[i]["openDate"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = data[i]["unit"]
                companyname=(data[i]["company_name"])
                issuefor = "General Public" 
                # check the company name contains '[' or not 
                if "[" in companyname:
                    companyname=companyname.split("[")[0]
                    issuefor = data[i]["company_name"].split("[")[1].split("]")[0]
                    if issuefor == "FPO":
                        issuefor = "General Public"
                symbol = data[i]["symbol"]
                issuetype='IPO'
                issuemanager = data[i]['issueManager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    # pass
                    # print(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)
                    # WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)
                    pass

# Handeling the Mutual Fund Data
def MutualFundHandeling(data):
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["closeDate"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            # if closingdate >= today:
            if True:
                openingdate = data[i]["openDate"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = data[i]["unit"]
                companyname=data[i]["company_name"]
                issuefor = "General Public" 
                symbol = data[i]["symbol"]
                issuetype='Mutual Fund'
                issuemanager = data[i]['issueManager']
                if not issuemanager:
                    issuemanager='Self Managed'
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    pass
                    print(f"Closig Date : {closingdate}\nOpening Date : {openingdate}\nTotal Issue Unit : {totalissueunit}\nCompany Name : {companyname}\nSymbol : {symbol}\nIssue Type : {issuetype}\nIssue For : {issuefor}\nIssue Manager : {issuemanager}")
                    # WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)
                    # pass

# Handeling the Debenture Data
def DebentureHandeling(data):
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["closeDate"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            # if closingdate >= today:
            if True:
                openingdate = data[i]["openDate"]
                # converting the opening date to date format
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit = data[i]["unit"]
                companyname=data[i]["company_name"]
                issuefor = "General Public" 
                symbol = data[i]["symbol"]
                issuetype='Mutual Fund'
                issuemanager = data[i]['issueManager']
                if not issuemanager:
                    issuemanager='Self Managed'
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    pass
                    # WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager)
                    # pass


def FilterData(response):
    # Filter the data
    data = response
    # print(data)
    # RightShare(data["Right Share"][0]['open'])
    # RightShare(data["Right Share"][2]['approved'])
    # IPOHandeling(data["IPO"][0]["open"])
    # IPOHandeling(data["IPO"][2]["approved"])
    # MutualFundHandeling(data["Mutual Fund"][0]['open'])
    # MutualFundHandeling(data["Mutual Fund"][2]['approved'])

    DebentureHandeling(data["Debentures"][1]['close'])

# def WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager):
#     if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
#         # Storing in the Database
#         query=f"INSERT INTO ipodetails(openingdate,closingdate,totalissueunit,companyname,symbol,issuetype,issuefor,issuemanager) VALUES('{openingdate}','{closingdate}',{totalissueunit},'{companyname}','{symbol}','{issuetype}','{issuefor}','{issuemanager}');"
#         print(query)
#         cursor.execute(query)
#     print("Data Written to Database")


if __name__ == "__main__":
    api_url="https://sarallagani.xyz/api/ipo/get/all"
    get_api_data(api_url)
    # connection.commit()
