# ### streamlit run main.py
import os
import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO

from claude import is_chart, analyze_img
from utils import encode_img, data_to_telegram
from voice import text_to_parags, parags_to_speech

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

                if st.button("Play voice"):
                    if response:
                        parags = text_to_parags(response)
                        output_audio = parags_to_speech(parags)

                        # Create a BytesIO object from the audio data
                        audio_data = BytesIO(output_audio)

                        # Display the audio player
                        st.audio(audio_data, format='audio/mp3')

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