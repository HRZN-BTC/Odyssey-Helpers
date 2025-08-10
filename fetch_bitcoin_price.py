import os
import requests
from datetime import datetime
from supabase import create_client, Client

def fetch_bitcoin_price():
    """Fetch Bitcoin price from CoinMarketCap API and store in Supabase"""
    
    # Get environment variables
    CMC_API_KEY = os.getenv('CMC_API_KEY')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    if not all([CMC_API_KEY, SUPABASE_URL, SUPABASE_KEY]):
        raise ValueError("Missing required environment variables")
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # CoinMarketCap API request
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
        'Accept': 'application/json'
    }
    params = {
        'symbol': 'BTC'
    }
    
    try:
        # Fetch data from CoinMarketCap
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract Bitcoin data
        btc_data = data['data']['BTC']
        quote_data = btc_data['quote']['USD']
        
        # Prepare data for database
        bitcoin_price_data = {
            'price': quote_data['price'],
            'last_updated': datetime.utcnow().isoformat(),
            'percent_change_24h': quote_data['percent_change_24h']
        }
        
        # Insert data into Supabase
        result = supabase.table('bitcoin_price').update(bitcoin_price_data).eq('id', 1).execute()
        
        print(f"Successfully stored Bitcoin price: ${quote_data['price']:.2f}")
        print(f"24h change: {quote_data['percent_change_24h']:.2f}%")
        print(f"Record ID: {result.data[0]['id'] if result.data else 'Unknown'}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinMarketCap: {e}")
        return False
    except Exception as e:
        print(f"Error storing data in Supabase: {e}")
        return False

if __name__ == "__main__":
    success = fetch_bitcoin_price()
    if not success:
        exit(1)