import requests
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "evolution_api")
BOT_URL = os.getenv("BOT_URL", "http://localhost:8000")

def setup_webhook():
    """Setup webhook in Evolution API"""
    webhook_url = f"{BOT_URL}/webhook/"
    print("=" * 60)
    print("🔧 Webhook Setup Tool")
    print("=" * 60)
    print(f"Evolution API URL: {EVOLUTION_API_URL}")
    print(f"Instance: {INSTANCE_NAME}")
    print(f"Webhook URL: {webhook_url}")
    print("=" * 60)
    
    url = f"{EVOLUTION_API_URL}/webhook/set/{INSTANCE_NAME}"
    
    headers = {
        "apikey": EVOLUTION_API_KEY
    }
    
    # Minimal events for our use case
    payload = {
        "url": webhook_url,
        "webhook_by_events": True,
        "webhook_base64": False,
        "events": [
            "APPLICATION_STARTUP",
            "MESSAGES_UPSERT",
            "CONNECTION_UPDATE",
            "QRCODE_UPDATED"
        ]
    }
    
    try:
        print(f"\n📤 Sending webhook setup request...")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Webhook setup successful!")
            print(json.dumps(result, indent=2))
        else:
            print(f"\n❌ Webhook setup failed!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

def check_webhook():
    """Check current webhook configuration"""
    url = f"{EVOLUTION_API_URL}/webhook/find/{INSTANCE_NAME}"
    headers = {"apikey": EVOLUTION_API_KEY}
    
    try:
        print(f"\n🔍 Checking current webhook configuration...")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Current webhook configuration:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Failed to check webhook: {response.text}")
    except Exception as e:
        print(f"Error checking webhook: {e}")

def delete_webhook():
    """Delete webhook configuration"""
    url = f"{EVOLUTION_API_URL}/webhook/delete/{INSTANCE_NAME}"
    headers = {"apikey": EVOLUTION_API_KEY}
    
    try:
        print(f"\n🗑️  Deleting webhook configuration...")
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"✅ Webhook deleted successfully!")
        else:
            print(f"❌ Failed to delete webhook: {response.text}")
    except Exception as e:
        print(f"Error deleting webhook: {e}")

if __name__ == "__main__":
    # Check if API key is set
    if not EVOLUTION_API_KEY:
        print("❌ Please set EVOLUTION_API_KEY in .env file")
        sys.exit(1)
    
    print("Evolution API Webhook Management")
    print("=" * 60)
    
    # Show current webhook
    check_webhook()
    
    print("\nOptions:")
    print("1. Setup new webhook")
    print("2. Delete webhook")
    print("3. Check webhook status")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        print(f"\nSetting up webhook to: {BOT_URL}/webhook/")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            setup_webhook()
        else:
            print("Operation cancelled.")
    elif choice == "2":
        confirm = input("\nAre you sure you want to delete the webhook? (yes/no): ")
        if confirm.lower() == 'yes':
            delete_webhook()
        else:
            print("Operation cancelled.")
    elif choice == "3":
        check_webhook()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid option.")