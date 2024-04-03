import os
import base64
import requests


# Bot token from env
bot_token = os.environ['BOT_TOKEN']

def encode_img(photo):
    image_data = photo.getvalue()
    file_extension = photo.name.split(".")[-1].lower()
    encoded_image = base64.b64encode(image_data).decode()

    if file_extension in ["jpg", "jpeg"]:
        media_type = "image/jpeg"

    elif file_extension == "png":
        media_type = "image/png"

    else:
        media_type = None

    return encoded_image, media_type



def data_to_telegram(response, photo):
    # Send the photo first
    photo_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {"photo": photo.getvalue()}
    payload = {"chat_id": "-4161262764"}
    photo_response = requests.post(photo_url, data=payload, files=files)

    if photo_response.status_code == 200:
        # If photo sent successfully, send the text
        text_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": "-4161262764",
            "text": response
        }
        requests.post(text_url, json=payload)
