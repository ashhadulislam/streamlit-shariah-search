# https://analyticsindiamag.com/how-to-implement-convolutional-autoencoder-in-pytorch-with-cuda/
# https://stackoverflow.com/questions/59924310/load-custom-data-from-folder-in-dir-pytorch

import numpy as np
import os
import time
import copy
import os
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfReader
import pandas as pd


from torchvision import datasets, models, transforms


def get_similar_articles(q, df,vectorizer):
    print("query:", q)
    # Convert the query become a vector
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    sim_ = {}
    # Calculate the similarity
    for i in range(df.shape[1]):        
        val=np.dot(df.loc[:, str(i)].values, q_vec) / np.linalg.norm(df.loc[:, str(i)]) * np.linalg.norm(q_vec)        
        sim_[i] = val
    # Sort the values 
    sim_sorted = sorted(sim_.items(), key=lambda x: x[1], reverse=True)
    # Print the articles and their similarity values    
    the_pages=[]
    for k, v in sim_sorted:
#         print(k)
        if v > 0.0 or v<0:
            # print("Page",k,"text:",documents_clean[k])
            the_pages.append(k)
            # print()    
    the_pages.sort()
    return the_pages


def get_selected_pdf(the_pages,q1):
    reader = PdfReader("data/Shariaa-Standards-ENG.pdf")
    savepath="output/"+q1+".pdf"


    pdf_writer = PdfFileWriter()
    for start_page in the_pages:
        start = start_page
        end = start+1
        while start<end:
            pdf_writer.addPage(reader.getPage(start))
            start+=1
    with open(savepath,'wb') as out:
        pdf_writer.write(out)    

    return savepath



