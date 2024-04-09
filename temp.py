import streamlit as st
from PIL import Image
import anthropic
import base64
import io

# Assuming your Anthropics API key is set up in Streamlit’s secrets
anthropic_api_key = st.secrets["anthropic_api"]
client = anthropic.Anthropic(api_key=anthropic_api_key)

def process_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="you're a helpful assistant, you need to help the user to extract specific information from the given input source from the user precisely. \ngive the requested information from the user in an informative way.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": img_str
                        }
                    },
                    {
                        "type": "text",
                        "text": "\ni have uploaded a receipt, can you tell me all the information you see in a structured way?"
                    }
                ]
            }
        ]
    )
    return response.content

def main():
    # Enhanced UI/UX
    st.sidebar.header("App Navigation")
    st.sidebar.info("This is a demo application to showcase image processing with AI. Upload an image, and let AI do the magic!")
    
    st.title("AI-Powered Image Processing App")
    st.markdown("Welcome to this AI-powered image processing application. Please upload an image to get started.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        
        with st.expander("Preview Image"):
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        if st.button("Process Image"):
            with st.spinner('Processing...'):
                image = Image.open(uploaded_file)
                response = process_image(image)
                st.success("Processing complete!")
                st.write(response)
            st.balloons()  # Add a little celebration effect

    st.markdown("---")
    st.markdown("<h6 style='text-align: center; color: gray;'>AI Image Processing App © 2024</h6>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
