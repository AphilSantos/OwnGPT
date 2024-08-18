import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

# Function to generate QR code
def generate_qr_code(link, name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    if name:
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)
        
        # Load a larger font
        try:
            font = ImageFont.truetype("segoeui.ttf", 40)  # Load a font with size 20
        except IOError:
            font = ImageFont.load_default()  # Fallback to default if font not found
        
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create a new image with adjusted height (30px padding below, 0px above)
        img_with_text = Image.new('RGB', (img.width, img.height + text_height + 30), 'white')  # Only 30px padding below
        img_with_text.paste(img, (0, 0))
        
        # Position text with no padding above and 30px padding below
        text_position = ((img.width - text_width) // 2, img.height)
        draw = ImageDraw.Draw(img_with_text)
        draw.text(text_position, name, fill="black", font=font)
        
        return img_with_text
    return img



# Streamlit app UI
st.title("QR Code Generator")

# User input: URL link
link = st.text_input("Enter the link for which to generate the QR code:")

# User input: Name to display below QR code
name = st.text_input("Enter a name to display below the QR code (optional):")

# Generate QR code button
if st.button("Generate QR Code"):
    if link:
        qr_image = generate_qr_code(link, name)
        
        # Display QR code
        st.image(qr_image, caption="Generated QR Code", use_column_width=True)
        
        # Download QR code as PNG
        buf = io.BytesIO()
        qr_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download QR Code",
            data=byte_im,
            file_name="qr_code.png",
            mime="image/png"
        )
    else:
        st.error("Please enter a link to generate the QR code.")
