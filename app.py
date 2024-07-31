import streamlit as st
import pickle
from feature_extraction import PhishingURLDetector

# Loading the model
model = pickle.load(open('xgboost_model.pkl', 'rb'))
detector = PhishingURLDetector(model)

# Streamlit app
st.title("Phishing Website Detector")

# Input URL from the user
url = st.text_input('Enter the full URL')

# Predict button
if st.button('Predict'):
    if url:
        input_data = detector.extract_features(url)
        prediction = model.predict(input_data)
        
        # st.write(input_data)
        
        if prediction[0] == 1:
            st.success('The website is **legitimate**.')
        else:
            st.error('The website is **suspicious**.')
    else:
        st.error('Please enter a URL.')
    