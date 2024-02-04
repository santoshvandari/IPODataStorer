from bs4 import BeautifulSoup
import requests,datetime,psycopg2

# Defining the URL and fetching the data from the website
url="https://www.nepsebajar.com/ipo-pipelinewewe"
req=requests.get(url)
soup=BeautifulSoup(req.text, "html.parser")
print(soup.prettify())
tabledata=soup.select("table#example tbody tr")

# Connecting With The Database 
# Database connection
connectionString = "postgres://postgres.xirdbhvrdyarslorlufu:9XEq4EPhvJzDXfA7@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
try:
    connection = psycopg2.connect(connectionString)
    cursor = connection.cursor()
    cursor.execute('truncate ipoinfodetails;')
    print("Connected to PostgreSQL database successfully!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

print(tabledata)

date=datetime.date.today()
counter=0
for data in tabledata:
    if counter>=11:
        break
    counter+=1
    # Retrieving the Data and cleaning it
    companyname = (data.select_one('td:nth-child(1) a').text).strip()
    symbol = (data.select_one('td:nth-child(2) a').text).strip()
    totalissueunit = int((data.select_one('td:nth-child(3)').text).strip())
    issuetypeinfo=(data.select_one('td:nth-child(4)').text).strip()
    if issuetypeinfo.find('-')!=-1:
        issuetypeinfo=issuetypeinfo.split('-')[1]
    
    if issuetypeinfo.find('For')!=-1:
        issuetype = issuetypeinfo.split('For')[1]
    else:
        issuetype = issuetypeinfo
    issuemanager=(data.select_one('td:nth-child(5)').text).strip()
    openingdatestr = (data.select_one('td:nth-child(6)').text).strip().replace('/','-')
    openingdate = datetime.datetime.strptime(openingdatestr, '%Y-%m-%d').date()
    closingdatestr = (data.select_one('td:nth-child(7)').text).strip().replace('/','-')
    closingdate = datetime.datetime.strptime(closingdatestr, '%Y-%m-%d').date()
    # print(companyname,symbol,totalissueunit,issuetype,issuemanager,openingdate,closingdate)
    print(f"Company Name: {companyname}\nSymbol: {symbol} \nTotal Issue Unit: {totalissueunit} \nIssue Type: {issuetype} \nIssue Manager: {issuemanager} \nOpening Date: {openingdate} \nClosing Date: {closingdate}\n\n")

    # with open('test.txt', 'a') as f:
    #     f.write(f"Company Name: {companyname}\nSymbol: {symbol} \nTotal Issue Unit: {totalissueunit} \nIssue Type: {issuetype} \nIssue Manager: {issuemanager} \nOpening Date: {openingdate} \nClosing Date: {closingdate}\n\n")

    # check all are not empty
    if companyname and symbol and totalissueunit and issuetype and issuemanager and openingdate and closingdate:
        # if(closingdate>=date):
        if(True):
            query=f"INSERT INTO ipoinfodetails VALUES('{companyname}','{symbol}',{totalissueunit},'{issuetype}','{issuemanager}','{openingdate}','{closingdate}');"
            print(query)
            # print(query)
            cursor.execute(query)

connection.commit()