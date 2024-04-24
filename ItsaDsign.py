import streamlit as st
from datetime import datetime
from PIL import Image
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "CV.pdf"

profile_pic = current_dir / "assets" / "aaron3.jpg"

# --- general settings ---

PAGE_TITLE = "Digital Resume | Aaron Santos"
PAGE_ICON = ":wave"
NAME = "Aaron Santos"
DESCRIPTION = """
Senior Web Designer & Developer, creating profitable ecommerce websites.
"""

EMAIL = "aphilvs@gmail.com"
SOCIAL_MEDIA = {
    "Facebook":"https://web.facebook.com/aaronphil2z.santos/",
    "ItsaD'sign":"https://web.facebook.com/profile.php?id=100088701973298",
    "LinkedIn":"https://www.linkedin.com/in/aaron-phil-santos-a1561b22b/",
    "Github":"https://github.com/AphilSantos"
}   

st.set_page_config(page_title=PAGE_TITLE,page_icon=PAGE_ICON)

# --- load css, pdf, profile pic ---

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)

# ---head section ---
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label=":newspaper: Download Resume",
        data=PDFbyte,
        file_name=resume_file.name,
        mime="application/octet-stream",
    )
    st.write(":email:",EMAIL)

st.write("#")
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f":pushpin: [{platform}]({link})")

st.write("#")
st.subheader("Experiences & Qualifications")
st.write(
    """
- :muscle: 3 years experience designing and developing Ecommerce Websites using Wordpress, Wix, Shopify, Squarespace, and System.io
- :muscle: Good experience in team collaboration leading to customer confidence and satisfaction as lead/assistant developer
- :muscle: Reliable at identifying and solving internal problems in the program in terms of conversion performance and product delivery

    """
)

st.write("#")
st.subheader("Hard Skills")
st.write(
    """
- :desktop_computer: Competitive Programming: JavaScript(HTML DOM), Python(Flask, Streamlit, Django), C#, Shopify Liquid, PHP
- :frame_with_picture: Professional Front-End Design: Figma, Canva, HTML, CSS
- :mega: Excellent English Communicator, College Mathematics
    """
)

#JOb 1
st.write("#")
st.subheader("Work History")
st.write(":school: **BYU-Pathway Worldwide | Mentor and Student Support Agent**")
st.write("July 2023 - Present")
st.write(
    """
    - :arrow_forward: Providing solutions for students and help to become familiar with the new online education platform
    - :arrow_forward: Developed ways to help fellow mentors in their work to reach students by creating my own Send Burst App
    - :arrow_forward: Flexible and dependable. Flexi working hours strategy to accomodate students from all over the world
    """
)
st.write("---")

#Job2
st.write("#")
st.write(":school: **I Help Create/Itsa'Dsign | Freelance Web developer**")
st.write("July 2021 - Present")
st.write(
    """
    - :arrow_forward: Started web development career by maintaining client websites and repairs
    - :arrow_forward: Excellent client relations by providing productivity solutions for better conversion
    - :arrow_forward: Communicator: 90% success rate in closing deals with customers by good service presentatins and product delivery
    """
)
st.write("---")

#Job3
st.write("#")
st.write(":school: **BrandLume | Junior Web Developer**")
st.write("Juanuary 2023 - November 2023")
st.write(
    """
    - :arrow_forward: Excellent customer service by providing cost-effective development strategies for diverse client needs
    - :arrow_forward: Flexible designs for unique client needs and goals. Believer of "No one size fits all." Customize is key to success.
    - :arrow_forward: Collaborator: Being a team-player is another key to success. 
    """
)
st.write("---")

st.write("#")
st.subheader("Contact Me")

contact_form = """
<form action="https://formsubmit.co/aphilvs@gmail.com" method="POST" style="display: flex; flex-direction: column; align-items: center;">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required style="width: 300px; padding: 5px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc;">
     <input type="email" name="email" placeholder="Your email" required style="width: 300px; padding: 5px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc;">
     <textarea name="message" placeholder="Your message here" style="width: 300px; height: 150px; padding: 5px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc;"></textarea>
     <button type="submit" style="padding: 10px 20px; border-radius: 5px; background-color: transparent; color: inherit; border: 1px; border-color: #E7E7E8; cursor: pointer;">Send Message</button>
</form>

"""


st.markdown(contact_form, unsafe_allow_html=True)



st.write("---")
st.write("© Aaron Santos | Data Science Portfolio")


