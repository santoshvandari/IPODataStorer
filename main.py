import requests

import datetime

def get_api_data(api_url):
    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the API response data
            # print("API Response:")
            # Check the Response is not NUll
            if response.json() is not None:            
                data=response.json()
                FilterData(data)
            else:
                print("Error: API Response is NULL")
        else:
            
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error: {e}")

def RightShare(data):
    for i in range(len(data)):
        closingdate=data[i]['closing_date']
        if closingdate:
            # closingdate=datetime.date.fromisoformat(closingdate)
            today=datetime.date.today()
            # if closingdate > today:
            if True:
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
    for i in range(len(data)):
        # print(data[i])
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
                issuetype='IPO'
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


def FPOHandeling():
    pass


def AuctionHandeling():
    pass

def MutualFundHandeling():
    pass



def FilterData(response):
    # Filter the data
    data = response
    RightShare(data["rights"])
    # IPOHandeling(data["ipo"])
    # print(data)
    # filtered_data = [item for item in data if item['status'] == 'active']
    # print("Filtered Data:")
    # print(data['ipo'][0]['company_name'])
    # print(filtered_data)


def WriteToDatabase():
    pass

if __name__ == "__main__":
    api_url="https://www.nepsealpha.com/api/smx9841/investment_calander"

    get_api_data(api_url)
