import requests

def get_api_data(api_url):
    try:
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the API response data
            print("API Response:")
            # print(response.json())
            data=response.json()
            FilterData(data)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error: {e}")


def FilterData(response):
    # Filter the data
    data = response
    # print(data)
    # filtered_data = [item for item in data if item['status'] == 'active']
    print("Filtered Data:")
    print(data['ipo'][0]['company_name'])
    # print(filtered_data)


def WriteToDatabase():
    pass

if __name__ == "__main__":
    api_url="https://www.nepsealpha.com/api/smx9841/investment_calander"

    get_api_data(api_url)
