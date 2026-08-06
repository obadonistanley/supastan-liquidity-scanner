import requests
import os


class TelegramBot:


    def __init__(self):

        self.token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )

        self.chat_id = os.getenv(
            "TELEGRAM_CHAT_ID"
        )


    def send(self, message):

        if not self.token or not self.chat_id:

            print(
                "Telegram credentials missing"
            )

            return False


        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )


        data = {

            "chat_id": self.chat_id,

            "text": message

        }


        try:

            response = requests.post(

                url,

                data=data,

                timeout=10

            )


            return response.status_code == 200


        except Exception as e:

            print(
                "Telegram error:",
                e
            )

            return False
