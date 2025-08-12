import os
import requests
from supabase import create_client, Client
import onesignal
from onesignal.api import default_api
from onesignal.model.notification import Notification
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# One Signal credentials
ONE_SIGNAL_APP_KEY = os.environ.get("ONE_SIGNAL_APP_KEY")
ONE_SIGNAL_APP_ID = os.environ.get("ONE_SIGNAL_APP_ID")

# GitHub raw file URL
BITTHOUGHTS_URL = "https://raw.githubusercontent.com/oogunjob/Daily-BitThought/refs/heads/main/bitthoughts.txt"

# OneSignal configuration
configuration = onesignal.Configuration(
    app_key=ONE_SIGNAL_APP_KEY,
)

def fetch_daily_bitthought():
    """
    Fetches the next daily bitthought from GitHub and updates the database.
    Returns the quote text or None if an error occurs.
    """
    try:        
        # Get current state from database
        current_record = supabase.table('daily_bitthought').select('*').eq('id', 1).execute()
        
        if not current_record.data:
            # First time setup - insert initial record
            current_line_number = 1
            print("No existing record found, starting from line 1")
        else:
            current_line_number = current_record.data[0].get('current_line_number', 1)
            print(f"Current line number: {current_line_number}")
        
        # Fetch the bitthoughts file from GitHub
        print(f"Fetching bitthoughts from: {BITTHOUGHTS_URL}")
        response = requests.get(BITTHOUGHTS_URL, timeout=10)
        response.raise_for_status()
        
        # Split into lines and filter out empty lines
        lines = [line.strip() for line in response.text.split('\n') if line.strip()]
        total_lines = len(lines)
        print(f"Total lines available: {total_lines}")
        
        if not lines:
            raise ValueError("No bitthoughts found in the file")
        
        # Get the current quote (adjust for 0-based indexing)
        line_index = (current_line_number - 1) % total_lines
        current_quote = lines[line_index]
        
        # Calculate next line number (wrap around to 1 if we reach the end)
        next_line_number = (current_line_number % total_lines) + 1
        
        print(f"Selected quote from line {current_line_number}: {current_quote[:50]}...")
        print(f"Next line number will be: {next_line_number}")
        
        # Update or insert the record in the database
        if not current_record.data:
            # Insert new record
            result = supabase.table('daily_bitthought').insert({
                'id': 1,
                'quote': current_quote,
                'current_line_number': next_line_number
            }).execute()
        else:
            # Update existing record
            result = supabase.table('daily_bitthought').update({
                'quote': current_quote,
                'current_line_number': next_line_number,
                'last_updated': 'now()'
            }).eq('id', 1).execute()
        
        if result.data:
            print("Successfully updated daily bitthought in database")
            return current_quote
        else:
            print("Failed to update database")
            return None
            
    except requests.RequestException as e:
        print(f"Error fetching bitthoughts from GitHub: {str(e)}")
        return None
    except Exception as e:
        print(f"Error in fetch_daily_bitthought: {str(e)}")
        return None

def send_update_daily_bitthought():
    """
    Sends daily Captain's Log notifications to users who have opted in.
    """
    try:
        # First, fetch and update the daily bitthought
        daily_quote = fetch_daily_bitthought()
        
        if not daily_quote:
            print("Failed to fetch daily bitthought. Aborting notification send.")
            return 0
        
        # Fetch users who have opted into daily captain's log notifications
        response = supabase.table('profiles').select('id').eq('notif_daily_captains_log', True).execute()
        
        if not response.data:
            print("No users found with daily captain's log notifications enabled.")
            return 0
            
        # Extract user IDs
        user_ids = [user['id'] for user in response.data]
        print(f"Found {len(user_ids)} users subscribed to daily captain's log notifications")
        
        # Create OneSignal API instance
        with onesignal.ApiClient(configuration) as api_client:
            api_instance = default_api.DefaultApi(api_client)
            
        # Create notification with the daily quote
        notification = Notification(
            app_id=ONE_SIGNAL_APP_ID,
            headings={"en": "Captain's Log 📜₿"},
            contents={"en": daily_quote},
            include_aliases={"external_id": user_ids},
            target_channel="push",
            ios_badge_type="Increase",
            ios_badge_count=1,
        )
        
        # Send notification
        api_instance.create_notification(notification)
        print(f"Sent notification with quote: {daily_quote[:50]}...")
        
        return len(user_ids)
            
    except Exception as e:
        print(f"Error sending daily captain's log notification: {str(e)}")
        return 0

if __name__ == "__main__":
    num_sent = send_update_daily_bitthought()
    if num_sent:
        print(f"Successfully sent daily bitthought notification to {num_sent} users")
    else:
        print("Failed to send notifications or no users to notify")