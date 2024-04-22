import streamlit as st
import smtplib
from email.message import EmailMessage
import ssl
import pandas as pd
import base64
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

#navigation using option_

# Define the send_email function
def send_email(recipient_name, recipient_email, subject, body_template, password):
    msg = EmailMessage()
    msg.set_content(body_template.replace("{name}", recipient_name).replace("{email}",recipient_email), subtype="html")
    msg["Subject"] = subject
    msg["From"] = sender_name
    msg["To"] = recipient_email

    context = ssl.create_default_context()

    # Gmail SMTP settings
    # email_ad = "aaron.santos.mentor@gmail.com"
    # email_password = "lhfspaztcqrewjuh"

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email_ad, password)
    server.send_message(msg)
    server.quit()

# Function to encode uploaded image to base64 for embedding in HTML
def get_image_base64(image):
    with open(image, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to add selected block to the email template
def add_block_to_template(block_type, content, template, label):
    if block_type == 'image':
        encoded_image = get_image_base64(content)
        img_tag = f'<img src="data:image/jpeg;base64,{encoded_image}" width="200"/>'
        template += img_tag + '<br>'
    elif block_type == 'quote':
        quote_tag = f'<blockquote>{content}</blockquote>'
        template += quote_tag + '<br>'
    elif block_type == 'link':
        link_tag = f'<a href="{content}">{label}</a>'
        template += link_tag + '<br>'
    return template

# Function to display the email template elements
def display_email_template(email_elements):
    email_template_html = ""
    for element in email_elements:
        if element['type'] == 'image':
            email_template_html += f'<img src="{element["content"]}" width="200"/><br>'
        elif element['type'] == 'quote':
            email_template_html += f'<blockquote>{element["content"]}</blockquote><br>'
        elif element['type'] == 'link':
            email_template_html += f'<a href="{element["content"]}">{element["Label"]}</a><br>'
    return email_template_html

# Streamlit UI components
st.set_page_config(layout="wide",

                   )
st.title("DesaBoom!!")

# Create two columns for the layout
col1, col2 = st.columns(2)

# Column for input fields for the email
with col1:
    sender_name = st.text_input("Sender Name")
    recipient_email = st.text_input("Recipient Email (optional)")
    subject = st.text_input("Email Subject")
    # Store the body template in the session state
    st.session_state.body_template = st.text_area("Email Body (HTML)", height=300)
    body_template = st.session_state.get('body_template', '')

    # Button to show the email preview
    if st.button('Preview Email'):
        # Using an expander to simulate a modal dialog
        with st.expander("Email Preview", expanded=True):
            components.html(st.session_state.body_template, height=3200)
    email_ad = st.text_input("Email Address", type="default")        
    password = st.text_input("Email Password", type="password")

    # When the 'Send Email' button is clicked, send the email
    if st.button("Send Email"):
        send_email(sender_name, recipient_email, subject, st.session_state.body_template, password)
        st.success(f"Email sent to {sender_name} at {recipient_email}")
# Column to display the email list and file uploader
with col2:
    st.write("Upload a CSV file for email list")
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        # Read the CSV into a DataFrame
        email_df = pd.read_csv(uploaded_file)

        # Display the DataFrame in the app
        st.write(email_df)

        # Assuming the DataFrame has 'Name' and 'Email' columns, send emails
        if st.button("Send Emails to List"):
            for index, row in email_df.iterrows():
                send_email(row['Name'], row['Email'], subject, st.session_state.body_template, password)
                st.write(f"Email sent to {row['Name']} at {row['Email']}")
            st.success("All emails sent")

# You can place this outside the columns if you want it to span the full width of the page
# if uploaded_file is not None and 'email_df' in locals():
#     st.write("Email List")
#     st.dataframe(email_df[['Name', 'Email']])


block_area, preview_area, block_edit = st.columns(3)

# Initialize session state for email elements
if 'email_elements' not in st.session_state:
    st.session_state.email_elements = []

# Column 1: Elements the user can select to add to the template
with block_area:
    st.subheader("Elements")
    # Image upload
    uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'], key='image_uploader')
    if uploaded_image is not None:
        encoded_image = get_image_base64(uploaded_image)
        image_html = f'data:image/jpeg;base64,{encoded_image}'
        st.session_state.email_elements.append({'type': 'image', 'content': image_html})

    # Add quote
    quote = st.text_input('Enter a quote')
    if st.button('Add Quote'):
        st.session_state.email_elements.append({'type': 'quote', 'content': quote})

    # Add link
    link = st.text_input('Enter a link URL')
    if st.button('Add Link'):
        st.session_state.email_elements.append({'type': 'link', 'content': link})

# Column 2: The working area to assemble the email template
with block_edit:
    st.subheader("Design Area")
    # Interactive block editing
    for i, element in enumerate(st.session_state.email_elements):
        with st.container():
            st.markdown(f"### {element['type'].title()} Block {i+1}")
            if element['type'] == 'image':
                st.image(element['content'], width=200)
            elif element['type'] == 'quote':
                new_quote = st.text_area(f"Quote {i+1}", value=element['content'], key=f'quote_{i}')
                st.session_state.email_elements[i]['content'] = new_quote
            elif element['type'] == 'link':
                new_link = st.text_input(f"Link {i+1}", value=element['content'], key=f'link_{i}')
                st.session_state.email_elements[i]['content'] = new_link
            if st.button(f"Remove {element['type'].title()} {i+1}", key=f'remove_{i}'):
                st.session_state.email_elements.pop(i)
                st.experimental_rerun()

# # Column 3: Additional options or preview of the email (not used)
# with preview_area:
#     st.subheader("Preview")

#     # Render the email template as HTML in the preview area
#     if st.session_state.body_template:  # only display if body_template is not empty
#         # Use the session state to render the preview
#         st.markdown(st.session_state.body_template, unsafe_allow_html=True)

# Column 3: Additional options or preview of the email
with preview_area:
    st.subheader("Email Preview")

    # If the body_template is not empty, render it
    if st.session_state.body_template:
        # Directly render HTML with components.html
        components.html(st.session_state.body_template, height=3200)

    # Render the email template as HTML
    for element in st.session_state.email_elements:
        if element['type'] == 'image':
            st.image(element['content'], width=200)
        elif element['type'] == 'quote':
            st.write(element['content'])
        elif element['type'] == 'link':
            st.markdown(f"[{element['content']}]({element['content']})", unsafe_allow_html=True)

# Clear button to clear the session state and reset the template
if st.button('Clear Template'):
    st.session_state.email_elements = []