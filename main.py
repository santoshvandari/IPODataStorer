import requests,datetime,psycopg2

def ConnectToDatabase():
    # Connect to the database
    pass

def get_api_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            if response.json():            
                data=response.json()
                FilterData(data)
            else:
                print("Error: API Response is NULL")
                exit(0)
        else:
            
            print(f"Error: {response.status_code} - {response.text}")
            exit(0)

    except Exception as e:
        print(f"Error: {e}")
        exit(0)

def RightShare(data):
    for i in range(len(data)):
        closingdate=data[i]['closing_date']
        if closingdate:
            # closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            if closingdate > today:
                openingdate=data[i]['opening_date']
                openingdate=datetime.date.fromisoformat(openingdate)
                totalissueunit=data[i]['units']
                companyname=data[i]['company_name']
                symbol=data[i]['symbol']
                issuetype='Right Share'
                issuefor = "General Public"
                issuemanager = data[i]['issue_manager']
                if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
                    pass
                    # message=f'''New {issuetype} of {companyname} is opening for {issuefor} from Today with total unit {totalissueunit}. Please Don't miss the chance to apply.

                    # Right Share Information:
                    # Company Name: {companyname}
                    # Symbol: {symbol}
                    # Issue Type: {issuetype}
                    # Issue For: {issuefor}
                    # Total Unit: {totalissueunit}
                    # Issue Manager: {issuemanager}
                    # Opening Date: {openingdate}
                    # Closing Date: {closingdate}'''
                    # print(message)


def IPOHandeling(data):
    i=0
    # for i in range(len(data)):
    if True:
        print(data[i])
        # Extracting the Closing Date 
        closingdate = data[i]["closing_date"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            # if closingdate > today:
            if True:
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
                    pass
                    # message=f'''New {issuetype} of {companyname} is opening for {issuefor} from Today with total unit {totalissueunit}. Please Don't miss the chance to apply.

                    # IPO Information:
                    # Company Name: {companyname}
                    # Symbol: {symbol}
                    # Issue Type: {issuetype}
                    # Issue For: {issuefor}
                    # Total Unit: {totalissueunit}
                    # Issue Manager: {issuemanager}
                    # Opening Date: {openingdate}
                    # Closing Date: {closingdate}'''
                    # print(message)


def FPOHandeling(data):
    # if True:
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["closing_date"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            # if closingdate > today:
            if True:
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
                    pass
                    # message=f'''New {issuetype} of {companyname} is opening for {issuefor} from Today with total unit {totalissueunit}. Please Don't miss the chance to apply.

                    # FPO Information:
                    # Company Name: {companyname}
                    # Symbol: {symbol}
                    # Issue Type: {issuetype}
                    # Issue For: {issuefor}
                    # Total Unit: {totalissueunit}
                    # Issue Manager: {issuemanager}
                    # Opening Date: {openingdate}
                    # Closing Date: {closingdate}'''
                    # print(message)


def AuctionHandeling(data):
    # print(data[i])
    # if True:
    for i in range(len(data)):
        # Extracting the Closing Date 
        closingdate = data[i]["close_date"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            # if closingdate > today:
            if True:
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
                    pass
                    # message=f'''New {issuetype} of {companyname} is opening for {issuefor} from Today with total unit {totalissueunit}. Please Don't miss the chance to apply.

                    # FPO Information:
                    # Company Name: {companyname}
                    # Symbol: {symbol}
                    # Issue Type: {issuetype}
                    # Issue For: {issuefor}
                    # Total Unit: {totalissueunit}
                    # Issue Manager: {issuemanager}
                    # Opening Date: {openingdate}
                    # Closing Date: {closingdate}'''
                    # print(message)


def MutualFundHandeling(data):
    # i=0
    # print(data[i]) 
    # if True:
    for i in range(len(data)):
        closingdate = data[i]["closing_date"]
        if closingdate:
            # converting the closing date to date format
            closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            # if closingdate > today:
            if True:
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
                    pass
                    message=f'''New {issuetype} of {companyname} is opening for {issuefor} from Today with total unit {totalissueunit}. Please Don't miss the chance to apply.

                    FPO Information:
                    Company Name: {companyname}
                    Symbol: {symbol}
                    Issue Type: {issuetype}
                    Issue For: {issuefor}
                    Total Unit: {totalissueunit}
                    Issue Manager: {issuemanager}
                    Opening Date: {openingdate}
                    Closing Date: {closingdate}'''
                    print(message)




def FilterData(response):
    # Filter the data
    data = response
    ConnectToDatabase()
    # RightShare(data["rights"])
    # IPOHandeling(data["ipo"])
    # FPOHandeling(data["fpo"])
    # AuctionHandeling(data["auction"])
    MutualFundHandeling(data["mutual_fund"])
   

def WriteToDatabase(closingdate, openingdate, totalissueunit, companyname, symbol, issuetype, issuefor, issuemanager):
    if closingdate and openingdate and totalissueunit and companyname and symbol and issuetype and issuefor and issuemanager:
        pass

if __name__ == "__main__":
    api_url="https://www.nepsealpha.com/api/smx9841/investment_calander"

    get_api_data(api_url)
