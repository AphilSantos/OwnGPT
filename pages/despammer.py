import streamlit as st
import requests
import time

# Function to send a test email
def send_test_email_to_contact_form(url, data, headers=None):
    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

# Streamlit App UI
st.title("Contact Form Spam Tester for WordPress Sites")

# Input fields for user to enter details
form_url = st.text_input("Contact Form URL", placeholder="Enter the URL of the contact form")
spam_attempts = st.number_input("Number of Test Submissions", min_value=1, max_value=100, value=10)
time_delay = st.number_input("Delay Between Submissions (in seconds)", min_value=0.0, value=1.0)

# Default form data (you can adjust these fields according to the form)
form_name = "Spam Bot"
form_email = "spam@example.com"
form_message = "This is a test spam message to verify the contact form."

# Button to start the spam test
if st.button("Start Spam Test"):
    if form_url:
        success_count = 0
        fail_count = 0
        
        for i in range(spam_attempts):
            st.write(f"Sending test submission {i+1}...")
            form_data = {
                "your-name": f"{form_name} {i+1}",
                "your-email": form_email,
                "your-message": form_message
            }
            
            success = send_test_email_to_contact_form(form_url, form_data)
            
            if success:
                success_count += 1
                st.success(f"Submission {i+1} successful!")
            else:
                fail_count += 1
                st.error(f"Submission {i+1} failed.")
            
            time.sleep(time_delay)
        
        st.write(f"Test Completed: {success_count} Successful, {fail_count} Failed.")
    else:
        st.error("Please provide the URL of the contact form.")
