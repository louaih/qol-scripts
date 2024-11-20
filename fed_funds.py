import requests

# Replace 'YOUR_API_KEY' with your actual FRED API key
FRED_API_KEY = '3dc10bed7b0213881b5d6ff6367df628'

def fetch_federal_funds_rate():
    api_url = f'https://api.stlouisfed.org/fred/series/observations?series_id=DFF&api_key={FRED_API_KEY}&file_type=json'
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

if __name__ == '__main__':
    rate = fetch_federal_funds_rate()
    if rate is not None:
        print(f'Current Federal Funds Rate: {rate}%')
