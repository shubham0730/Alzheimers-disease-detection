import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np

# Load the HDF5 model
model = load_model('my_model.h5')

# Define a function to make predictions on input images


def predict(image):
    # Resize the image to 176x176 pixels
    image = image.resize((176, 176))

    # Convert the image to a NumPy array and normalize the pixel values
    data = np.array(image).astype('float32') / 255.0

    # Add an extra dimension to the data to match the model's input shape
    data = np.reshape(data, (1, 176, 176, 3))

    # Make the prediction using the loaded model
    prediction = model.predict(data)

    # Return the prediction
    return int(prediction[0])


# Define the Streamlit app


def app():
    # Set the app title
    st.title('Alzheimer Detection App')

    # Upload an MRI image
    image_file = st.file_uploader(
        'Upload an MRI image', type=['png', 'jpg', 'jpeg'])

    # Make a prediction when an image is uploaded
    if image_file is not None:
        # Open the image file using PIL
        image = Image.open(image_file)

        # Resize and convert the image to a NumPy array
        img_array = np.array(image.resize((176, 208)))

        # Reshape the image array to have the correct shape
        # img_array = np.reshape(img_array, (1, 176, 176, 3))

        # Make a prediction on the image
        prediction = predict(img_array)

        # Display the prediction result
        if prediction == 1:
            st.write('The image shows signs of Alzheimer\'s disease')
        else:
            st.write('The image does not show signs of Alzheimer\'s disease')


# Run the Streamlit app
if __name__ == '__main__':
    app()
