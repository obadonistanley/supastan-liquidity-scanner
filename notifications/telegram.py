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
            print("Telegram credentials missing")
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



    def send_image(self, image_path, caption):

        if not self.token or not self.chat_id:
            print("Telegram credentials missing")
            return False


        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendPhoto"
        )


        try:

            with open(image_path, "rb") as image:

                files = {
                    "photo": image
                }

                data = {
                    "chat_id": self.chat_id,
                    "caption": caption
                }


                response = requests.post(
                    url,
                    data=data,
                    files=files,
                    timeout=20
                )


            return response.status_code == 200


        except Exception as e:

            print(
                "Telegram image error:",
                e
            )

            return False
