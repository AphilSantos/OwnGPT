import streamlit as st
from PIL import Image
import io
import base64

def resize_image(image, width=None, height=None, percent=None):
    if percent is not None:
        width = int(image.width * percent / 100)
        height = int(image.height * percent / 100)
    return image.resize((width, height), Image.Resampling.LANCZOS)

def get_image_download_link(img, filename='image', format='PNG'):
    """Generates a link allowing the PIL image to be downloaded in the specified format."""
    buffered = io.BytesIO()
    img_format = format.upper()
    if img_format == 'JPG':
        img_format = 'JPEG'
    img.save(buffered, format=img_format)
    byte_data = buffered.getvalue()
    b64 = base64.b64encode(byte_data).decode()
    href = f'<a href="data:image/{format.lower()};base64,{b64}" download="{filename}.{format.lower()}">Download as {format.upper()}</a>'
    return href

st.title('Image Resizer')

# Image upload
uploaded_files = st.file_uploader("Choose an image or images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'webp'])

# Resize options
resize_option = st.radio("Resize by:", ("Percent", "Pixels"))

if resize_option == "Percent":
    percent = st.slider("Percentage:", min_value=1, max_value=200, value=100)
else:
    width = st.number_input("Width (pixels):", min_value=1, value=100)
    height = st.number_input("Height (pixels):", min_value=1, value=100)

# File format selection
format_option = st.selectbox("Select download format:", ("PNG", "JPG", "WEBP"))

if st.button("Resize"):
    if not uploaded_files:
        st.warning("Please upload at least one image.")
    else:
        for uploaded_file in uploaded_files:
            # Display original image
            st.write("Original Image:")
            st.image(uploaded_file)

            # Resize and display new image
            image = Image.open(uploaded_file)
            if resize_option == "Percent":
                resized_image = resize_image(image, percent=percent)
            else:
                resized_image = resize_image(image, width=width, height=height)

            st.write("Resized Image:")
            # To display the resized image, we need to save it to a buffer first
            buf = io.BytesIO()
            resized_image.save(buf, format=format_option)
            st.image(buf, caption='Resized Image')
            
            # Download link
            st.markdown(get_image_download_link(resized_image, filename=uploaded_file.name.split('.')[0], format=format_option), unsafe_allow_html=True)