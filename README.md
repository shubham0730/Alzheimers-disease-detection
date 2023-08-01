# Alzheimers-disease-detection-
Deep learning project for detection of Alzheimer's disease based on 4 classes using MRI Scans using CNN
The dataset used in the project is from kaggle.
Dataset link: https://www.kaggle.com/datasets/tourist55/alzheimers-dataset-4-class-of-images

I have built a cnn model to detect the presence of dementia in a patient's MRI Scans. The accuracy the model achieved was 93.75% and data loss was seen to be 22.17%

![acc_ss](https://user-images.githubusercontent.com/71088263/233706569-3809db9a-6d9a-4697-86b2-75b7068e7825.png)

![loss_ss](https://user-images.githubusercontent.com/71088263/233706642-b277f939-f8d8-41ae-89d6-3ad036ea575b.png)

Then I have saved the model in h5 file format and the loaded it in a streamlit app to make the model accesible to users. 
![image](https://user-images.githubusercontent.com/71088263/233707755-ce40e927-6518-41fd-a756-242150f332bc.png)

The form is completely validated. 
![output1](https://user-images.githubusercontent.com/71088263/233706839-fc05612d-2924-49c4-b5aa-024ce64fbde0.png)

![image](https://user-images.githubusercontent.com/71088263/233711336-90953eef-b33d-43b8-a9b5-4057f1b4eae8.png)


After submitting your details the web app generates a pdf report using fpdf and your data gets stored in a mysql database
