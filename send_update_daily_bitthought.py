import os
from supabase import create_client, Client
import onesignal
from onesignal.api import default_api
from onesignal.model.notification import Notification

# Supabase credentials
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# One Signal credentials
ONE_SIGNAL_APP_KEY = os.environ.get("ONE_SIGNAL_APP_KEY")
ONE_SIGNAL_USER_KEY = os.environ.get("ONE_SIGNAL_USER_KEY")
ONE_SIGNAL_APP_ID = os.environ.get("ONE_SIGNAL_USER_KEY")

# OneSignal configuration
configuration = onesignal.Configuration(
    app_key=ONE_SIGNAL_APP_KEY,
    user_key=ONE_SIGNAL_USER_KEY,
)

def send_update_daily_bitthought():
    """
    Sends daily Captain's Log notifications to users who have opted in.
    """
    try:
        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Fetch users who have opted into daily captain's log notifications
        response = supabase.table('profiles').select('id').eq('notif_daily_captains_log', True).execute()
        
        if not response.data:
            print("No users found with daily captain's log notifications enabled.")
            return
            
        # Extract user IDs
        user_ids = [user['id'] for user in response.data]
        print(f"Found {len(user_ids)} users subscribed to daily captain's log notifications")
        
        # Create OneSignal API instance
        with onesignal.ApiClient(configuration) as api_client:
            api_instance = default_api.DefaultApi(api_client)
            
            # Create notification
            notification = Notification(
                app_id=ONE_SIGNAL_APP_ID,
                headings={"en": "Captain's Log"},
                contents={"en": "Ahoy matey, ship sailing"},
                include_aliases={"external_id": user_ids},
                target_channel="push",
                ios_badge_type="Increase",
                ios_badge_count=1,
            )
            
            # Send notification
            api_response = api_instance.create_notification(notification)
            print(f"Notification sent successfully! Response: {api_response}")
            
            return len(user_ids)
            
    except Exception as e:
        print(f"Error sending daily captain's log notification: {str(e)}")
        return 0

if __name__ == "__main__":
    num_sent = send_update_daily_bitthought()
    if num_sent:
        print(f"Successfully sent daily captain's log notification to {num_sent} users")
    else:
        print("Failed to send notifications or no users to notify")