import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
from streamlit_option_menu import option_menu
import re
import base64
from fpdf import FPDF

import mysql.connector

# Connect to the MySQL database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database="Alzheimers"
    )
    print("Database connection successful")
except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit(1)
# Get a cursor object to execute SQL queries
mycursor = mydb.cursor()




st.markdown("""
<style>
    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}
</style>""",
unsafe_allow_html=True)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-position: center;
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('./images/bg3.png')

# Load the saved model
model = tf.keras.models.load_model('model.h5')

# Define the class labels
class_labels = ['Mild Demented', 'Moderate Demented',
                'Non Demented', 'Very Mild Demented']

# Define the function to preprocess the image


def preprocess_image(image):
    image = image.convert('RGB')
    image = image.resize((176, 176))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Define the Streamlit app

def validate_phone_number(phone_number):
    """
    Validates that a phone number is a 10-digit number.
    """
    pattern = r'^\d{10}$'
    contact=re.match(pattern, str(phone_number))
    if not contact:
        st.error('Please enter a 10 digit number!')
        return False
    return True

def validate_name(name):
    if not all(char.isalpha() or char.isspace() for char in name):
        st.error("Name should not contain numbers or special character.")
        return False
    return True

def validate_input(name, age,contact,file):
    if not name:
        st.error('Please enter the patients name!')
        return False
    if not age:
        st.error('Please enter your age!')
        return False
    if not contact:
        st.error('Please enter your contact number!')
        return False
    if not file:
        st.error('Please upload the MRi Scan!')
        return False
    return True
#with st.sidebar:
selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Alzhiemer Detection", "About US"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
if selected =='Home':
    def app():
     st.title("Alzheimer's Disease")
     st.write("Alzheimer disease is the most common type of dementia. It is a progressive disease beginning with mild memory loss and possibly leading to loss of the ability to carry on a conversation and respond to the environment. Alzheimer disease involves parts of the brain that control thought, memory, and language.")
     st.write("Using this website, you can find out that does your MRI scan have Alzheimer's disease. It is classified according to four different stages of Alzheimer's disease.")
     st.write('1. Mild Demented')
     st.write("2. Very Mild Demented")
     st.write("3. Moderate Demented")
     st.write("4. Non Demented")

if selected =='About US':
    def app():
        st.title('Welcome!')
        st.write('This web app uses a CNN model to recognize the presence of Alzheimer diasease in any age group. Leaving behind the traditional method of MRI Scans you can now get yourself checked through our protable web APP and you can get your report within no time.')
        st.write('This web app is a MINi Project made by Shubham Shinde')

if selected=='Alzhiemer Detection':
  def app():
    st.title('Alzheimer Detection Web App')
    st.write('Please enter your personal details along with MRI scan.')

    # Add fields for name, age, contact, and gender
    with st.form(key='myform', clear_on_submit=True):
        name = st.text_input('Name')
        age = st.number_input('Age', min_value=1, max_value=150, value=40)
        gender = st.radio('Gender', ('Male', 'Female','Other'))
        contact = st.text_input('Contact Number', value='', key='contact')

        file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])
        submit=st.form_submit_button("Submit")

        # Define a function to insert the form data into the `prediction` table
    def insert_data(name, age, gender, contact, prediction):
        try:
          sql = "INSERT INTO predictions (Patient_Name, Age, Gender, Contact, Prediction) VALUES (%s, %s, %s, %s, %s)"
          val = (name, age, gender, contact, prediction)
          mycursor.execute(sql, val)
          mydb.commit()
          print(mycursor.rowcount, "record inserted")
        except mysql.connector.Error as err:
          print("Error inserting record:", err)  

                
    if file is not None and validate_input(name, age,contact,file) and validate_phone_number(contact) and validate_name(name):
                  st.success('Your personal information has been recorded.', icon="✅")
                  image = Image.open(file)
                  png_image = image.convert('RGBA')
                  st.image(image, caption='Uploaded Image', width=200)
                  # Use the fields for name, age, contact, and gender in the output
        
                  st.write('Name:', name)
                  st.write('Age:', age)
                  st.write('Gender:', gender)
                  st.write('Contact:', contact)
                  image = preprocess_image(image)
                  prediction = model.predict(image)
                  prediction = np.argmax(prediction, axis=1)
                  st.success('The predicted class is: '+ class_labels[prediction[0]])
                  result_str = 'Name: {}\nAge: {}\nGender: {}\nContact: {}\nPrediction for Alzheimer: {}'.format(
                     name, age, gender, contact, class_labels[prediction[0]])
                  insert_data(name, age, gender, contact, class_labels[prediction[0]])
                  export_as_pdf = st.button("Export Report")

                  def create_download_link(val, filename):
                    b64 = base64.b64encode(val)  # val looks like b'...'
                    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'
        
                  if export_as_pdf:
                     pdf = FPDF()
                     pdf.add_page()
                     # set the border style
                     pdf.set_draw_color(0, 0, 0)
                     pdf.set_line_width(1)

                     # add a border to the entire page
                     pdf.rect(5.0, 5.0, 200.0, 287.0, 'D')
    
                     # Set font for title
                     pdf.set_font('Times', 'B', 24)
                     pdf.cell(200, 20, 'Alzheimer Detection Report', 0, 1, 'C')
    
                     # Set font for section headers
                     pdf.set_font('Arial', 'B', 16)
                     pdf.cell(200, 10, 'Patient Details', 0, 1)
    
                     # Set font for regular text
                     pdf.set_font('Arial', '', 12)
                     pdf.cell(200, 10, f'Name: {name}', 0, 1)
                     pdf.cell(200, 10, f'Age: {age}', 0, 1)
                     pdf.cell(200, 10, f'Gender: {gender}', 0, 1)
                     pdf.cell(200, 10, f'Contact: {contact}', 0, 1)
                     pdf.ln(0.15)
                     pdf.ln(0.15)



                     # Add the image to the PDF object's images dictionary
                     png_file = "image.png"
                     png_image.save(png_file, "PNG")
                     pdf.cell(200, 10, 'MRI scan:', 0, 1)
                     pdf.image(png_file, x=40, y=80, w=50,h=50)
                     pdf.ln(0.15)
                     pdf.ln(10.0)
                     pdf.ln(10.0)
                     pdf.ln(10.15)
                     pdf.ln(10.15)
                     pdf.ln(1.15)
                     pdf.ln(1.15)
                     pdf.ln(1.15)

                     # Set font for prediction text
                     pdf.set_font('Arial', 'B', 16)
                     pdf.cell(200, 10, f'Prediction for Alzheimer: {class_labels[prediction[0]]}', 0, 1)
                     pdf.ln(2.0)
                     pdf.set_font('Arial', 'B', 12)
                     if (prediction!=2):
                      pdf.set_text_color(255, 0, 0)
                      pdf.cell(200,10,'Demetia detected in your MRI, kindly consult a nearby neurologist immediately!',0,1)
                      pdf.set_text_color(0, 0, 255)
                      pdf.set_font('Arial', 'B', 10)
                      pdf.cell(200, 10, 'Here are some precautions you can take:', 0, 1, 'C')
                      pdf.ln(2)

                      precautions = [
                        '1. Stay mentally active: Engage in mentally stimulating activities such as reading, writing, puzzles, and games to keep your brain active.',
                        '2. Stay physically active: Exercise regularly to improve blood flow to the brain and help prevent cognitive decline.',
                        '3. Eat a healthy diet: Eat a balanced diet that is rich in fruits, vegetables, whole grains, and lean protein to help maintain brain health.',
                        '4. Stay socially active: Engage in social activities and maintain social connections to help prevent social isolation and depression.',
                        '5. Get enough sleep: Aim for 7-8 hours of sleep per night to help improve brain function and prevent cognitive decline.'                ]
        
                      pdf.set_font('Arial', '', 12)

                      for precaution in precautions:
                       pdf.multi_cell(190, 10, precaution, 0, 1, 'L')
                       pdf.ln(1)
          
                     else:
                       pdf.set_text_color(0, 255, 0)
                       pdf.cell(200,10,'Congratulations! There is no sign of demetia in your MRI.',0,1)
    
                      # Create and display the download link
                     html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")
                     st.markdown(html, unsafe_allow_html=True)





# Run the app
if __name__ == '__main__':
    app()