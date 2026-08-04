import requests
import os


class TelegramBot:


    def __init__(self):

        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")



    def send(self, message):

        if not self.token or not self.chat_id:
            return "Telegram not configured"



        url = (
            f"https://api.telegram.org/bot"
            f"{self.token}/sendMessage"
        )


        data = {
            "chat_id": self.chat_id,
            "text": message
        }


        response = requests.post(
            url,
            data=data
        )


        return response.json()
