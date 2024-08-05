import streamlit as st
import pickle
from feature_extraction import PhishingURLDetector

# Loading the model
model = pickle.load(open('xgboost_model.pkl', 'rb'))
detector = PhishingURLDetector(model)

# Streamlit app
st.title("Phish Link Finder")

st.write('''
         Detect phishing links using this machine learning application by entering their URL.
         ''')

# Input URL from the user
url = st.text_input('URL',placeholder='Enter the full URL',label_visibility="collapsed")

# Predict button
if st.button('Predict'):
    if url:
        input_data = detector.extract_features(url)
        prediction = model.predict(input_data)
        
        if prediction[0] == 1:
            st.success('The website is **legitimate**.')
        else:
            st.error('The website is **suspicious**.')
    else:
        st.error('Please enter a URL.')
      
from footer import footer
st.markdown(footer,unsafe_allow_html=True)