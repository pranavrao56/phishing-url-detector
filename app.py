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
        
        if prediction[0] == 1:
            st.success('The website is **legitimate**.')
        else:
            st.error('The website is **suspicious**.')
    else:
        st.error('Please enter a URL.')
    
footer="""<style>
a:link , a:visited{
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: blue;
background-color: transparent;
text-decoration: none;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
text-align: center;
}

</style>
<div class="footer">
<p>Developed by <a href="https://www.github.com/pranavrao56/" target="_blank">Pranav Rao</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)