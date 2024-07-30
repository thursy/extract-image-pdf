import os
import time
import tempfile
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
import fitz

bucket_staging = "cos-staging-onboard-1"
bucket_parsing = "cos-parsing-onboard-1"
bucket_knowledge = "cos-knowledge-onboard-1"
#============================GET CREDENTIALS===================================
load_dotenv()
cred_cos = {
        "COS_APIKEY": os.getenv("COS_APIKEY", None),
        "COS_INSTANCE_CRN": os.getenv("COS_INSTANCE_CRN", None),
        "endpoint_url_private": os.getenv("endpoint_url_private", None),
        "endpoint_url_public": os.getenv("endpoint_url_public", None),
    }


if None in cred_cos.values():
    print("Ensure you copied the .env file that you created earlier into the same directory as Main Page file")
    print("Check the credentials related to Cloud Object Storage")
else:
    st.session_state['creds_cos'] = cred_cos

#==========================IMPORT FROM UTILS===============================
from utils.cosmetic import *
from utils.cosresources import *
from utils.parsing import *
#==========================STREAMLIT PAGE CONFIG===============================
page_config()
#=============================STREAMLIT SIDE BAR===============================
with st.sidebar:
    st.markdown("Upload a document to store it to the knowledge based")
    uploaded_file = st.file_uploader("Source File:", accept_multiple_files=False, type=["pdf"])
#==============================STREAMLIT ELEMENT===============================
###==============================HEADER ATTRIBUTES================================
page_navbar()
###===========================UPLOADEDFILE CONTENT=============================  
if uploaded_file:
    with st.spinner('Wait for it...'):
        print(cred_cos)
        res = cos_init(creds=cred_cos)
        avail_bucket = get_buckets(res)

        if bucket_staging in avail_bucket:
            st.write(avail_bucket)
        
    #st.write(type(uploaded_file))

    with st.spinner('Upload file to cloud object storage...'):
        upload_fileobj(bucket_staging, uploaded_file.name, uploaded_file.getvalue(), res)

        file_info = {"upload_time": datetime.now(),
         "filename": uploaded_file.name,
         }

        obj_list = get_bucket_contents(bucket_staging,res)
        filename_exist = [obj['filename'] for obj in obj_list]

        print(filename_exist)
        if uploaded_file.name in filename_exist:
            st.success(f'Done...! {uploaded_file.name} is uploaded...!')
        else:
            st.write(obj_list)
            st.write(type(obj_list))

    
    with st.spinner(f'Parsing the {uploaded_file.name}...'):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file.seek(0)

            df_pdf, img_list, img_bin = parsing_pdf(temp_file, uploaded_file.name, bucket_parsing, cred_cos['endpoint_url_public'], res)

            st.write(df_pdf)
            file_info['img_list'] = img_list
            file_info['img_bin'] = img_bin
            st.write(file_info)

            image_thumbnail_grid(img_bin, img_list)

            df_pdf.to_csv(f'files/txt/{uploaded_file.name.split(".")[0]}.txt', sep='\t', index=False)



    with st.spinner('Upload result to cloud object storage...'):
        upload_file(bucket_knowledge, f'{uploaded_file.name.split(".")[0]}.txt', f'files/txt/{uploaded_file.name.split(".")[0]}.txt', res)

        file_info ["upload_time_txt"] = datetime.now()
        file_info ["filename_txt"] = f'{uploaded_file.name.split(".")[0]}.txt'
        
        obj_list = get_bucket_contents(bucket_knowledge,res)
        filename_exist = [obj['filename'] for obj in obj_list]

        print(filename_exist)
        if f'{uploaded_file.name.split(".")[0]}.txt' in filename_exist:
            st.success(f'Done...! Result is uploaded...!')
        else:
            st.write(obj_list)
            st.write(type(obj_list))
        
        st.write(file_info)
