import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def fetch_federal_funds_rate():
    api_url = f'https://api.stlouisfed.org/fred/series/observations?series_id=DFF&api_key={getenv("FRED_API_KEY")}&file_type=json'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        rate = data['observations'][-1]['value']
        return rate
    except requests.exceptions.RequestException as e:
        print('Error fetching Federal Funds Rate:', e)
        return None
    except (KeyError, IndexError) as e:
        print('Invalid data format from API:', e)
        return None

def fetch_marcus_rate(url):
    try:
        # Define headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Send a GET request to the URL with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element with the specified ID
        target_element = soup.find('div', {'id': 'text-5497986c7c'})

        # Extract the text content containing the percentage
        #print(target_element.text.split(' ')[2][-5:-1]+"%")
        percentage_text = target_element.text.split(' ')[2][-5:-1]+"%"

        return percentage_text

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__" :
    print("====== Marcus Savings Rate Grabber ======")
    rate = fetch_federal_funds_rate()
    if rate is not None:
        print(f'Current Federal Funds Rate: {rate}%')

    url = 'https://www.marcus.com/us/en'
    result = fetch_marcus_rate(url)
    if result:
        print(f"Marcus HYSA Rate: {result}")
    else:
        print("Failed to retrieve the percentage.")

    print(f"Difference: {(float(result[:-2])-float(rate)):.2f}%")
