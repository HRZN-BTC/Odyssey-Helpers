import os
import requests
from datetime import datetime
from supabase import create_client, Client

def fetch_bitcoin_price():
    """Fetch Bitcoin price from CoinGecko API and store in Supabase"""
    
    # Get environment variables
    CG_API_KEY = os.getenv('CG_API_KEY')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    
    if not all([CG_API_KEY, SUPABASE_URL, SUPABASE_KEY]):
        raise ValueError("Missing required environment variables")
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # CoinGecko API request
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    headers = {
        'x-cg-pro-api-key': CG_API_KEY,
        'Accept': 'application/json'
    }
    
    try:
        # Fetch data from CoinGecko
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract Bitcoin data
        price = data['market_data']['current_price']['usd']
        high_24h_usd = data['market_data']['high_24h']['usd']
        low_24h_usd = data['market_data']['low_24h']['usd']
        percent_change_24h = data['market_data']['price_change_percentage_24h']
        price_change_24h = data['market_data']['price_change_24h']
        
        # Prepare data for database
        bitcoin_price_data = {
            'price': price,
            'last_updated': datetime.utcnow().isoformat(),
            'percent_change_24h': round(percent_change_24h, 3),
            '24h_high': high_24h_usd,
            '24h_low': low_24h_usd,
            'price_change_24h': price_change_24h
        }
        
        # Update data in Supabase
        _ = supabase.table('bitcoin_price').update(bitcoin_price_data).eq('id', 1).execute()
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return False
    except Exception as e:
        print(f"Error storing data in Supabase: {e}")
        return False

if __name__ == "__main__":
    success = fetch_bitcoin_price()
    if not success:
        exit(1)
