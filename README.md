# extract-image-pdf
extract image from pdf and upload it to IBM Cloud Object Storage

## Credentials you need to provide

- COS_APIKEY
- COS_INSTANCE_CRN
- endpoint_url_private (eg: s3.private.jp-tok.cloud-object-storage.appdomain.cloud)
- endpoint_url_public (eg: s3.jp-tok.cloud-object-storage.appdomain.cloud)

Note: In this project you will need 3 COS buckets:
1. Staging (to store the uplaoded PDF files)
2. Parsing (to store the images uploded)
3. Knowledge ( to store txt files that contain text along with URL of corresponding images)


## Run it locally

1. clone the project into your local
2. create python virtual environment

```python -m venv genai```

3. activate the virtual environment

```source genai/bin/activate```

4. install the requirement

```python -m pip install -r requirements.txt```

5. run the streamlit

```streamlit run Main_Page.py ```

## Expected Output

If you run it correcty, this Streamlit app will provide you this kind of output
