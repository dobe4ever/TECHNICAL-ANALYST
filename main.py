### streamlit run main.py

import streamlit as st
import anthropic
import base64
from PIL import Image

# Defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()

def encode_img(photo):
    image_data = photo.getvalue()
    encoded_image = base64.b64encode(image_data).decode()
    file_extension = photo.name.split(".")[-1].lower()
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
            # model="claude-3-haiku-20240307",
            # model="claude-3-sonnet-20240229",
            model="claude-3-opus-20240229",
            max_tokens=4000,
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

    
def main():
    # Page title
    st.title("Opinionated Intelligence")
    # st.subheader("Upload a screenshot of your TradingView chart & get an assesement based purely on technical analysis")
    st.write("""
### Upload any chart
             
Include or exclude elements like indicators, timeframes, drawings or asset name to control the information the AI can see. This forces an impartial analysis, driven purely by the technical analysis signals present in the chart.
""")
    # Image uploader
    photo = st.file_uploader(
        "", type=["jpg", "jpeg", "png"]
    )

    # Display uploaded photo
    if photo:
        img = Image.open(photo)
        st.image(img)

    # Submit button
    if st.button("Submit") and photo is not None:
        encoded_image, media_type = encode_img(photo)
        chart = is_chart(encoded_image, media_type)
        if chart == 'YES':
            response = analyze_img(encoded_image, media_type)       
            st.subheader("Response:")
            st.write(response)
        else : 
            st.subheader("ERROR:")
            st.write("Invalid image, ry again")            

if __name__ == "__main__":
    main()
    
### streamlit run main.py