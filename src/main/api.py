import os
import vonage
from dotenv import load_dotenv

load_dotenv()

VONAGE_API_KEY = os.environ.get("VONAGE_API_KEY")
VONAGE_API_SECRET = os.environ.get("VONAGE_API_SECRET")

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
sms = vonage.Sms(client)

response_data = sms.send_message(
    {
        "from": "Vonage APIs",
        "to": "37064821004",
        "text": "A text message sent using the Nexmo SMS API",
    }
)

if response_data["messages"][0]["status"] == "0":
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {response_data['messages'][0]['error-text']}")
