import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
import io

def show_analysis():
    st.title('Phishing Dataset Analysis')

    st.write('''
             This page showcases the analysis of the chosen dataset and the results of training multiple machine learning models to find out which one is the most suitable for the task of phishing url detection.
             ''')
    
    dataset_url = 'https://www.kaggle.com/datasets/shibumohapatra/book-my-show/data'
    
    st.write(f'This data was borrowed from Kaggle: {dataset_url}')
    
    # Loading the Data
    st.header('1. Loading the Data')
    df = pd.read_csv('dataset.csv')
    st.write('Dataset Head:')
    st.dataframe(df.head())

    # Exploratory Data Analysis
    st.header('2. Exploratory Data Analysis')
    st.write(f'There are {df.shape[0]} rows and {df.shape[1]} columns in the dataset.')
    st.write('Features:')
    st.write(df.columns)
    st.write('Dataset Info:')
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    st.write('Number of Unique Values:')
    st.write(df.nunique())
    st.write('Checking for Empty Values:')
    st.write(df.isnull().sum().sort_values(ascending=False))
    df = df.drop('index', axis=1)
    st.write('Dataset Description:')
    st.write(df.describe().T)

    # Visualizing the Data
    st.header('3. Visualizing the Data')
    st.subheader('Univariate Analysis')
    fig, ax = plt.subplots(figsize=(20, 15))
    df.hist(bins=50, figsize=(20, 15), ax=ax)
    st.pyplot(fig)

    st.subheader('Correlation Heatmap')
    fig, ax = plt.subplots(figsize=(18, 18))
    sns.heatmap(df.corr(), annot=True, linewidths=.5, fmt='.1f', ax=ax)
    st.pyplot(fig)

    st.subheader('Phishing Count in Pie Chart')
    fig, ax = plt.subplots()
    df['Result'].value_counts().plot(kind='pie', autopct='%1.2f%%', ax=ax)
    ax.set_title("Phishing Count")
    st.pyplot(fig)

    # Splitting the Data
    st.header('4. Splitting the Data')
    X = df.drop(columns='Result', axis=1)
    y = df['Result']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    st.write(f'Train set shape: {X_train.shape}, {y_train.shape}')
    st.write(f'Test set shape: {X_test.shape}, {y_test.shape}')

    # Comparing Machine Learning Models
    st.header('5. Comparing Machine Learning Models')
    def train_and_evaluate_models(X_train, X_test, y_train, y_test):
        models = {
            "Logistic Regression": LogisticRegression(),
            "k-Nearest Neighbors": KNeighborsClassifier(),
            "Support Vector Classifier": SVC(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(),
            "XGBoost": XGBClassifier()
        }
        
        results = []
        
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            results.append({
                "Model": model_name,
                "Accuracy": accuracy,
                "F1 Score": f1
            })
        
        return pd.DataFrame(results)

    results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    results = results.sort_values(by=['Accuracy', 'F1 Score'], ascending=False).reset_index(drop=True)
    st.write('Model Evaluation Results:')
    st.dataframe(results)

    # Conclusion
    st.header('6. Conclusion')
    st.write('Decided to use the XGBoost Classifier model as its accuracy score and f1 score are the highest.')
