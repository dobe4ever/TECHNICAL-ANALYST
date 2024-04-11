import os
import re
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
    payload = {"chat_id": "-4158249275"}
    photo_response = requests.post(photo_url, data=payload, files=files)

    if photo_response.status_code == 200:
        # If photo sent successfully, send the text
        text_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": "-4158249275",
            "text": response
        }
        requests.post(text_url, json=payload)


def get_tag(tag, string, strip=False):
    t = re.findall(f"<{tag}>(.?)</{tag}>", string, re.DOTALL)
    if strip:
        t = [e.strip() for e in t]
    return t

def remove_empty_tags(text):
    return re.sub(r'<(\w+)></\1>$', '', text)

# def get_prompt(metaprompt_response):
#     between_tags = get_tag("Instructions", metaprompt_response)[0]
#     return remove_empty_tags(remove_empty_tags(between_tags).strip()).strip()

# def get_variables(prompt):
#     pattern = r'{([^}]+)}'
#     variables = re.findall(pattern, prompt)
#     return set(variables)

    # text = remove_empty_tags(t)
    # chart_details = re.search(r'<chart details>(.*?)</chart details>', text, re.DOTALL).group(1)
    # chart_analysis = re.search(r'<chart analysis>(.*?)</chart analysis>', text, re.DOTALL).group(1)
    # key_chart_info = get_tag("key chart inf", text, strip=True)
    # expected_market_behaviour = get_tag("expected market behaviour", text, strip=True)
    # prediction_and_confidence = get_tag("prediction and confidence", text, strip=True)
    # invalidation_conditions = get_tag("invalidation conditions", text, strip=True)
    # final = f"{key_chart_info}{expected_market_behaviour}{prediction_and_confidence}{invalidation_conditions}"