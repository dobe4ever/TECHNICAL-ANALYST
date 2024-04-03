# ### streamlit run main.py
import os
import time
import streamlit as st
import anthropic
import base64
from PIL import Image
import requests

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()

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


def is_chart(encoded_image, media_type):
    if encoded_image:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            temperature=0,
            system="<context>\nImage classification\n</context>\n\n<task>\nOnly respond \"YES\" or \"NO\" (Without quotes)\n\nIs the image provided one of the following charts:\n\nCandlestick\nBar\nLine\nPoint and Figure\nRenko\nKagi\nEquivolume\nTick\nA chart where technical analysis can be performed\n</task>",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        response = message.content[0].text
        print(response)
        return str(response)
    else:
        return "No image uploaded."

def analyze_img(encoded_image, media_type):
    if encoded_image:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            # model="claude-3-sonnet-20240229",
            # model="claude-3-opus-20240229",
            max_tokens=2500,
            temperature=0,
            system="<context>Technical analysis</context>\n\ntask>Your task is to analyze the chart provided and write a comprehensive assessment based solely on technical analysis, without considering any information other than what's visible on the chart.</task>",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        response = message.content[0].text
        return str(response)
    else:
        return "No image uploaded."


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


def main():
    # Page title
    st.markdown("## Opinionated Intelligence")
    st.markdown("### Upload any chart\n\nInclude or exclude elements like indicators, timeframes, drawings or asset name to control the information the AI can see. This forces an impartial analysis, driven purely by the technical analysis signals present in the chart.")

    # Image uploader
    photo = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    # Display uploaded photo and run analysis
    if photo:
        st.image(Image.open(photo))
        # with st.spinner("Uploading image..."):
        #     st.write("Valid image uploaded")
        with st.spinner("Doing technical analysis..."):
            encoded_image, media_type = encode_img(photo)
            chart = is_chart(encoded_image, media_type)
            if chart == 'YES':
                response = analyze_img(encoded_image, media_type)
                data_to_telegram(response, photo)
                st.success("Success!")
                st.markdown("### Response:")
                st.markdown(response)
            else:
                st.error("Only technical analysis charts accepted, try again.")
    else:
        st.info("Please upload an image to get started.")

if __name__ == "__main__":
    main()
    
### streamlit run main.py
    

g="""
git add . 

git commit -m "v0.1" 

git push origin master
"""
    
### streamlit run main.py