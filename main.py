import streamlit as st
from PIL import Image
from claude import img_class_asst
from utils import encode_img, data_to_telegram

def main():
    # Page title
    st.markdown("## Opinionated Intelligence")
    st.markdown("### Upload any chart\n\nInclude or exclude elements like indicators, timeframes, drawings or asset name to control the information the AI can see. This forces an impartial analysis, driven purely by the technical analysis signals present in the chart.")  # noqa: E501
    # Initialize session state variables
    # if "image" not in st.session_state:
    st.session_state.image = None
# if "response" not in st.session_state:
    st.session_state.response = None

    # Image uploader
    photo = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

    # Display uploaded photo and run analysis if photo
    if photo:
        st.session_state.image = Image.open(photo)
        st.image(st.session_state.image)

        with st.spinner("Doing technical analysis..."):
            encoded_image, media_type = encode_img(photo)
            if encoded_image:
                ta = img_class_asst(encoded_image, media_type)
                data_to_telegram(ta, photo)
                st.success("Success!")
                st.markdown("### Response:")
                st.markdown(ta)
            else:
                st.error("Only technical analysis charts accepted, try again.")
    else:
        st.info("Please upload an image to get started.")

if __name__ == "__main__":
    main()
    
### streamlit run main.py