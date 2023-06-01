# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 12:23:26 2023

@author: WIN
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import time
import hashlib
import pandas as pd
import numpy as np
from PIL import Image



def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password)==hashed_text:
        return hashed_text
    return False

import sqlite3
conn=sqlite3.connect('data.db')
c=conn.cursor()

#db functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password)')
    conn.commit()
    
def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()
    
    
def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall() 
    for i in data:
        print(i)
    return data

def readSqliteTable():
    try:
        sqliteConnection=sqlite3.connect('data.db')
        cursor=sqliteConnection.cursor()
        print("Connected to SQlite")
        sqlite_select_query="""SELECT * from userstable"""
        cursor.execute(sqlite_select_query)
        records=cursor.fetchall()
        print("The number of registered users are: ",len(records))
        for row in records:
            print("Username: ",row[0])
            print("Hashed Password: ",row[1])
            print("\n")
    except sqlite3.Error as error:
        print("Failed to read data from database",error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Connection is closed")

def main():
    
    image = Image.open('C:/Users/Shruti/Downloads/Multiple_Disease_Prediction_system/disease-prediction-logo.jpg')
    st.image(image)
    
    st.sidebar.text("ALready have account then signin/login else signup")
    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)
    
    
    if choice == "Home":
        st.sidebar.subheader("Home") 
        image = Image.open('C:/Users/Shruti/Downloads/Multiple_Disease_Prediction_system/Doctor.jpg')
        st.image(image)
            
    elif choice == "Login":
        
        st.sidebar.subheader("Login Section")
        username=""
        password=""
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Enter the Password to login",type='password')
        if st.sidebar.checkbox("Login"):
			# if password == '12345':
                create_usertable()
                hashed_pswd = make_hashes(password)

                result = login_user(username,check_hashes(password,hashed_pswd))
                if result:
                    st.sidebar.success("Logged In Successfully")
                    mul_dis_pred()
                else:
                    st.warning("Incorrect Username/Password")
    elif choice =="SignUp":
        image = Image.open('C:/Users/Shruti/Downloads/Multiple_Disease_Prediction_system/Doctor.jpg')
        st.image(image)
        st.sidebar.subheader("Create new Account")
        new_user=""
        new_password=""
        new_user=st.sidebar.text_input("Username")
        new_password=st.sidebar.text_input("Password",type='password')
        
        if st.sidebar.button("Create"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.sidebar.success("You have successfully created the new account")
            st.sidebar.info("Go to login menu to login")

def mul_dis_pred():
    readSqliteTable()
    diabetes_model = pickle.load(open('C:/Users/Shruti/Downloads/Multiple_Disease_Prediction_system/saved_models/diabetes.sav','rb'))
    
    heart_disease_model = pickle.load(open('C:/Users/Shruti/Downloads/Multiple_Disease_Prediction_system/saved_models/heart_disease.sav','rb'))
    
    breast_cancer_model = pickle.load(open('C:/Users/Shruti/Downloads/Multiple_Disease_Prediction_system/saved_models/breast_cancer.sav','rb'))
    
    
    # sidebar for navigation
    selected = option_menu('Multiple Disease Prediction System using ML',
                           ['Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Breast Cancer Prediction'],
                           orientation="horizontal",
                           icons=['activity','heart','gender-ambiguous'],
                           
                           default_index=0)        
    
    # diabetes prediction page
    if (selected=='Diabetes Prediction'):
        
        # page title
        st.title('Diabetes Prediction')
        
        #getting the input data from the user
        col1,col2,col3=st.columns(3)
        
        with col1:
            Age = st.text_input('Age')
        
        with col2:
            if st.selectbox("Gender",["Select","Male","Female"])=="Male":
                Gender=1
            else:
                Gender=0
                
        with col3:
            if st.selectbox("Polyuria",["Select","Yes","No"])=="Yes":
                Polyuria=1
            else:
                Polyuria=0
        
        with col1:
            if st.selectbox("Polydipsia",["Select","Yes","No"])=="Yes":
                Polydipsia=1
            else:
                Polydipsia=0
        
        with col2:
            if st.selectbox("Weight_loss",["Select","Yes","No"])=="Yes":
                Weight_loss=1
            else:
                Weight_loss=0
        
        with col3:
            if st.selectbox("Itching",["Select","Yes","No"])=="Yes":
                Itching=1
            else:
                Itching=0
        
        with col1:
            if st.selectbox("Irritability",["Select","Yes","No"])=="Yes":
                Irritability=1
            else:
                Irritability=0
        
        with col2:
            if st.selectbox("Delayed_healing",["Select","Yes","No"])=="Yes":
                Delayed_healing=1
            else:
                Delayed_healing=0
        
        with col3:
            if st.selectbox("Partial_paresis",["Select","Yes","No"])=="Yes":
                Partial_paresis=1
            else:
                Partial_paresis=0
        
        with col1:
            if st.selectbox("Alopecia",["Select","Yes","No"])=="Yes":
                Alopecia=1
            else:
                Alopecia=0
        
        #code for prediction
        #button
        with st.spinner('Wait for it...'):
            time.sleep(2)
        if st.button('Diabetes Test Result'):
            diagnosis=diabetes_model.predict([[Age,Gender,Polyuria,Polydipsia,Weight_loss,Itching,Irritability,Delayed_healing,Partial_paresis,Alopecia]])
            print(diagnosis)
            if (diagnosis[0]==1):
                st.error('So sorry to say that! The person has high chance of Diabetes')
            else:
                st.snow()
                st.success('Yay! The person has low chances of Diabetes')
            

        
      
    
    if (selected=='Heart Disease Prediction'):
        
        # page title
        st.title('Heart Disease Prediction')
        
        col1,col2,col3=st.columns(3)
        
        with col1:
            age=st.text_input('Age')
        
        with col2:
            if st.selectbox("Gender",["Select","Male","Female"])=="Male":
                sex=1
            else:
                sex=0
        
        with col3:
            cp=st.text_input('Chest Pain Type')
            
        with col1:
            trestbps=st.text_input('Resting Blood Pressure')
        
        with col2:
            chol=st.text_input('Serum cholestrol in mg/dl')
            
        with col3:
            if st.selectbox("Fasting Blood Sugar> 120mg/dl",["Select","Yes","No"])=="Yes":
                fbs=1
            else:
                fbs=0
        
        with col1:
            if st.selectbox("Resting Electrocardiographic results",["Select","Yes","No"])=="Yes":
                restecg=1
            else:
                restecg=0
        
        with col2:
            thalach=st.text_input('Maximum Heart Rate')
            
        with col3:
            if st.selectbox("Exercise induced angina",["Select","Yes","No"])=="Yes":
                exang=1
            else:
                exang=0
        
        with col1:
            oldpeak=st.text_input('Old peak')
        
        with col2:
            slope=st.text_input('ST/heart rate slope')
        
        with col3:
            ca=st.text_input('Calcium Score')
            
        with col1:
            thal=st.text_input('Thalassemia')
            
        #code for prediction
        #button
        with st.spinner('Wait for it...'):
            time.sleep(2)
        if st.button('Result for Heart Disease'):
            diagnosis=heart_disease_model.predict([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
            print(diagnosis)
            if (diagnosis[0]==1):
                st.error('The person has high chances of Heart Disease')
                
            else:
                st.snow()
                st.success('The person has low chances of Heart Disease')
        
        
        
    if (selected=='Breast Cancer Prediction'):
        
        # page title
        st.title('Breast Cancer Prediction')
        
        col1,col2,col3=st.columns(3)
        
        with col1:
            radius_mean=st.number_input('Radius Mean value')
        
        with col2:
            texture_mean=st.number_input('Texture Mean value')
            
        with col3:
            perimeter_mean=st.number_input('Perimeter Mean value')
            
        with col1:
            area_mean=st.number_input('Area Mean value')
        
        with col2:
            smoothness_mean=st.number_input('Smoothness Mean value')
            
        with col3:
            compactness_mean=st.number_input('Compactness Mean value')
            
        with col1:
            concavity_mean=st.number_input('Concavity Mean value')
        
        with col2:
            concavepoints_mean=st.number_input('Concave points Mean value')
            
        with col3:
            symmetry_mean=st.number_input('Symmetry Mean value')
        
        with col1:
            fractal_dimension_mean=st.number_input('Fractal Dimension Mean value')
            
        with col2:
            radius_se=st.number_input('Radius se value')
            
        with col3:
            texture_se=st.number_input('Texture se value')
        
        with col1:
            perimeter_se=st.number_input('Perimeter se value')
            
        with col2:
            area_se=st.number_input('Area se value')
            
        with col3:
            smoothness_se=st.number_input('Smoothness se value')
        
        with col1:
            compactness_se=st.number_input('Compactness se value')
            
        with col2:
            concavity_se=st.number_input('Concavity se value')
            
        with col3:
            concavepoints_se=st.number_input('Concave points se value')
        
        with col1:
            symmetry_se=st.number_input('Symmetry se value')
            
        with col2:
            fractal_dimension_se=st.number_input('Fractal dimension se value')    
            
        with col3:
            radius_worst=st.number_input('Radius worst value')
            
        with col1:
            texture_worst=st.number_input('Texture Worst value')
        
        with col2:
            perimeter_worst=st.number_input('Perimeter Worst value')
            
        with col3:
            area_worst=st.number_input('Area worst value')    
            
        with col1:
            smoothness_worst=st.number_input('Smoothness Worst value')
        
        with col2:
            compactness_worst=st.number_input('Compactness Worst value')
            
        with col3:
            concavity_worst=st.number_input('Concavity Worst value')
            
        with col1:
            concavepoints_worst=st.number_input('Concave points worst value')
        
        with col2:
            symmetry_worst=st.number_input('Symmetry worst value')
            
        with col3:
            fractal_dimension_worst=st.number_input('Fractal dimension worst value')
            
        #code for prediction
        #button
        with st.spinner('Wait for it...'):
            time.sleep(2)
        if st.button('Result for Breast Cancer'):
            diagnosis=breast_cancer_model.predict([[radius_mean,texture_mean,perimeter_mean,area_mean,smoothness_mean,compactness_mean,concavity_mean,concavepoints_mean,symmetry_mean,fractal_dimension_mean,radius_se,texture_se,perimeter_se,area_se,smoothness_se,compactness_se,concavity_se,concavepoints_se,symmetry_se,fractal_dimension_se,radius_worst,texture_worst,perimeter_worst,area_worst,smoothness_worst,compactness_worst,concavity_worst,concavepoints_worst,symmetry_worst,fractal_dimension_worst]])
            print(diagnosis)
            if (diagnosis[0]==1):
                st.error('Breast cancer is more likely to be Malignant')
                st.write('Malignant tumors can grow rapidly, invade and destroy nearby normal tissues, and spread throughout the body.')
            else:
                st.success('Breast cancer is more likely to be Benign')
                st.write('Benign tumors tend to grow slowly and do not spread.Hence it is also called as non cancerous')
        
if __name__=='__main__':
    main()