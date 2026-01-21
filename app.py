import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
import datetime as dt
# Let's configure the model
gemini_api_key = os.getenv("GOOGLE-API-19jan-key2")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Let's create sidebar for image upload
st.sidebar.title(":red[Upload Image]")
uploaded_image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg","png","jfif"],accept_multiple_files=True)
uploaded_image = [Image.open(img) for img in uploaded_image] 
if uploaded_image:
    st.sidebar.success('Image has been loaded successfully')
    
    st.sidebar.subheader(':blue[Uploaded Image]')
    st.sidebar.image(uploaded_image)
    
# Let's create the main page
st.title(':orange[DEFECT_FINDERAI:-] :blue[AI Assisted Structural Defect Identifier]')
st.markdown("### :green[Upload images of structural defects to identify & get solution using AI.]")
title = st.text_input("Enter Title for Defect Analysis Report:")
name = st.text_input("Enter Reporter's Name:")
organisation = st.text_input("Enter the Organization Name:")
designation = st.text_input("Enter the Designation of the Reporter:")
if st.button('Submit'):
    with st.spinner('Processing...'):
        prompt = f'''<Role> You are a structural engineer with 20+ years of experience in civil construction industry.
        <Goal> You need to prepare a detailed report on the structural defects shown in the images uploaded by the user.
        <Context> The images shared by the user has been attached.
        <Format> Follow the steps to prepare the report.
        * Add title at the top of the report. The title provided by the user is: {title}
        * Add name, designation and organisation of the reporter provided by the user. Also, include the date. Following are the details given by the user
        name: {name}
        designation: {designation}
        organisation: {organisation}
        date: {dt.datetime.now().date()}
        * Identify and classify the defect for eg: Crack, Spalling,Corrosion,Honeycombing etc. 
        * There could be more than one defect in images. Identify all of them separately.
        * For each identified defect, provide a short description of the defects measuring the severity as low,medium and high with its potential impact on the structure.
        * Also, the defect is inevitable or has been caused by malpractices or misuses. 
        * Finally, list the remedies or suggestions that can be adopted to fix the issue for each defect for repairing it to keep it intact for both the short-term and long-term horizon.
        * Also, give a rough estimate of the time and money it will take to fix all the issues.
        * Lastly, state the precautionary measures to be taken to avoid these defects in future.
        <Instructions> Use bullet points and tables for explanation wherever required.
        * The report generated should be in MS_Word format.
        * Make sure the report doesn't exceed 2 pages.
        '''
        response = model.generate_content([prompt,*uploaded_image],generation_config={'temperature':0.8})
        st.write(response.text)
    if st.download_button(label='Click to Download',data = response.text,file_name='structural defect report.txt',mime = 'text/plain'):
        st.success('Your file is downloaded')





