import streamlit as st
from lib import commons
import pandas as pd
import pickle

def app():
    header=st.container()
    
    
    with header:
        st.subheader("Enter search key words")
        search_words = st.text_input('Enter search words', '')

        if search_words!="":
            print("Going to search")
            df=pd.read_csv("data/Sharia-doc.csv",index_col=0)
            print(df.head())
            vectorizer = pickle.load( open( "models/vectorizer.p", "rb" ) )
            the_pages=commons.get_similar_articles(search_words, df,vectorizer)
            print("The pages are ",len(the_pages))
            save_path=commons.get_selected_pdf(the_pages,search_words)
            print("File is ",save_path)
            with open(save_path, "rb") as pdf_file:
                PDFbyte = pdf_file.read()

            st.download_button(label="Results for "+search_words,
                                data=PDFbyte,
                                file_name=search_words+".pdf",
                                mime='application/octet-stream')            

        