import os
import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO
from claude import is_chart, analyze_img
from utils import encode_img, data_to_telegram

def main():
    # Page title
    st.markdown("## Opinionated Intelligence")
    st.markdown("### Upload any chart\n\nInclude or exclude elements like indicators, timeframes, drawings or asset name to control the information the AI can see. This forces an impartial analysis, driven purely by the technical analysis signals present in the chart.")
    # Initialize session state variables
    if "image" not in st.session_state:
        st.session_state.image = None
    if "response" not in st.session_state:
        st.session_state.response = None

    # Image uploader
    photo = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    # Display uploaded photo and run analysis if photo
    if photo:
        st.session_state.image = Image.open(photo)
        st.image(st.session_state.image)

        with st.spinner("Doing technical analysis..."):
            encoded_image, media_type = encode_img(photo)
            chart = is_chart(encoded_image, media_type)
            if chart == 'YES':
                st.session_state.response = analyze_img(encoded_image, media_type)
                data_to_telegram(st.session_state.response, photo)
                st.success("Success!")
                st.markdown("### Response:")
                st.markdown(st.session_state.response)
            else:
                st.error("Only technical analysis charts accepted, try again.")

    # Display previous image and response if available
    elif st.session_state.image is not None:
        st.image(st.session_state.image)
        if st.session_state.response is not None:
            st.markdown("### Response:")
            st.markdown(st.session_state.response)

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