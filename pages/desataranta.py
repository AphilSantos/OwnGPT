import streamlit as st
import random
import string

# Function to generate random string
def generate_random_string(length, use_alphanumeric, use_special_characters):
    characters = ''
    
    if use_alphanumeric:
        characters += string.ascii_letters + string.digits
    
    if use_special_characters:
        characters += string.punctuation

    if not characters:
        return "No character types selected."

    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Streamlit app UI
st.title("Random String Generator")

# User input: Number of characters
length = st.number_input("Enter the number of characters:", min_value=1, value=8, step=1)

# User input: Character types
use_alphanumeric = st.checkbox("Include Alphanumeric Characters (a-z, A-Z, 0-9)", value=True)
use_special_characters = st.checkbox("Include Special Characters (@, #, $, etc.)")

# Generate button
if st.button("Generate Random String"):
    random_string = generate_random_string(length, use_alphanumeric, use_special_characters)
    st.write("Generated String:", random_string)
