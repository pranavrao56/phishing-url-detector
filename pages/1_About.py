import streamlit as st

st.title("About")

st.write('## What is Phishing?')

st.image('assets/URL_phishing_hero.png','Source: https://surfshark.com/blog/what-is-url-phishing')

st.write("""
         **Phishing** is a type of online scam where criminals send an email that appears to be from a legitimate company 
         and ask you to provide sensitive information. The information may then be used to access important accounts and 
         can result in identity theft and financial loss.

         Phishing websites are designed to trick you into thinking they are legitimate, often by using similar URLs, 
         logos, and other elements to mimic real websites. It's crucial to be cautious and verify the authenticity 
         of websites before entering any sensitive information.
        
         This Phishing Website Detector uses machine learning to analyze URLs and predict whether they are legitimate or suspicious.
         By inputting a URL, you can get an instant prediction about its legitimacy.
""")
