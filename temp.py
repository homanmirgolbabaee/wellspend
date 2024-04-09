import streamlit as st
from PIL import Image
import anthropic
import base64
import io

# Set your Anthropics API key here. In a real app, consider using st.secrets to securely manage your API key.
anthropic_api_key = st.secrets["anthropic_api"]

# Initialize the Anthropics client with your API key
client = anthropic.Anthropic(api_key=anthropic_api_key)

def process_image(image,prompt):
    # Convert the PIL image to a BytesIO buffer and then to a base64 encoded string
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Anthropics API call with the base64 encoded image
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
                        "text": prompt
                    }
                ]
            }
        ]
    )

    # Extract and return the API response
    return response.content

def main():
    st.title("Image Processing App")
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    prompt = st.text_input("Prompt")
    if uploaded_file is not None:
        # Convert the uploaded file to a PIL Image
        image = Image.open(uploaded_file)
        if st.button("Process"):
            # Process the image and get the response
            response = process_image(image,prompt)
            # Display the response on the page
            st.write(response)

if __name__ == "__main__":
    main()
