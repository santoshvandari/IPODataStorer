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

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def FilterData(response):
    # Filter the data
    data = response
    # print(data)
    # filtered_data = [item for item in data if item['status'] == 'active']
    print("Filtered Data:")
    print(data['ipo'])
    # print(filtered_data)




if __name__ == "__main__":
    # Replace 'YOUR_API_URL' with the actual API endpoint you want to request
    # api_url = input("Enter the API URL: ")
    api_url="https://www.nepsealpha.com/api/smx9841/investment_calander"

    get_api_data(api_url)
