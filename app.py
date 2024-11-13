import io
import DocTrans_Local2Blob
from distutils.log import debug
from fileinput import filename
from io import BytesIO
from PIL import Image
import getpass
from datetime import datetime
import time
import os
import socket

# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import time
import streamlit as st
import base64
import os

#To get the user ID
from streamlit.web.server.websocket_headers import _get_websocket_headers
 
headers = _get_websocket_headers()
username="demouser"
# if "X-Ms-Client-Principal-Name" in headers:
#     username = headers["X-Ms-Client-Principal-Name"]
 
# st.write(headers) # have a look at what else is in the dict

# Load the image
#image = Image.open("static/img/logo.png")

# Get the original image width and height
#original_width, original_height = image.size

# Calculate the new width to reduce the size to half
#new_width = int(original_width * 1.3)

# Resize the image
#image = image.resize((new_width, original_height))

# Display the resized image in the sidebar
#st.sidebar.image(image)

#Instructions :

# Display the instructions in the sidebar
st.sidebar.markdown("## Instructions:")
st.sidebar.write("1. Upload the document to translate")
st.sidebar.write("2. Type or select the languages")
st.sidebar.write("3. Click Translate to initiate the translation")
st.sidebar.write("4. Download the translated document")

# Display the release notes in the sidebar
st.sidebar.markdown("## Release Notes:")
st.sidebar.write("1. This Application works for most of the document formats (e.g., pdf, doc, ppt, xls, txt)")
st.sidebar.write("2. Translated document will have a suffix with the target language")

# Display the main title

st.markdown("<h1 style='text-align: left; font-size: 36px;'>Document Translator</h1>", unsafe_allow_html=True)

# Create a single file uploader widget with a unique key
st.write("")
count=1
uploaded_file = st.file_uploader("Upload a document to translate...", key=count)
count+=1

# Process the uploaded file as needed
if uploaded_file:


# Language selection

    st.write("")

# #short_language = st.selectbox("Select the target language for translation", ["Type or Select the Language", "English", "French", "German", "Vietnamese", "Chinese(Simplified)", "Dutch", "Italian", "Japanese", "Korean", "Polish", "Portuguese(Brazil)", "Portuguese(Portugal)", "Slovak", "Spanish", "Swedish"],key=count)
# short_language = st.selectbox("Select the target language for translation", ["Type or Select the Language", "English", "French", "German", "Vietnamese", 
#                    "Chinese(Simplified)", "Dutch", "Italian", "Japanese", "Korean", 
#                    "Polish", "Portuguese(Brazil)", "Portuguese(Portugal)", "Slovak", 
#                    "Spanish", "Swedish", "Traditional Chinese", "Czech", "Danish", "Finnish", "Canadian French", 
#                    "Indonesian", "Norwegian", "Russian", "Thai", "Turkish"],key=count)  
# #Dict = {'Type or Select the Language': None, 'English': 'en', 'French': 'fr', 'German': 'de', 'Vietnamese': 'vi', 'Chinese(Simplified)': 'zh-Hans', 'Dutch': 'nl', 'Italian': 'it', 'Japanese': 'ja', 'Korean': 'ko', 'Polish': 'pl', 'Portuguese(Brazil)': 'pt', 'Portuguese(Portugal)': 'pt-pt', 'Slovak': 'sk', 'Spanish': 'es', 'Swedish': 'sv'}
# Dict = {
#     'Type or Select the Language': None,
#     'English': 'en',
#     'French': 'fr',
#     'German': 'de',
#     'Vietnamese': 'vi',
#     'Chinese(Simplified)': 'zh-Hans',
#     'Dutch': 'nl',
#     'Italian': 'it',
#     'Japanese': 'ja',
#     'Korean': 'ko',
#     'Polish': 'pl',
#     'Portuguese(Brazil)': 'pt',
#     'Portuguese(Portugal)': 'pt-pt',
#     'Slovak': 'sk',
#     'Spanish': 'es',
#     'Swedish': 'sv',
#     'Traditional Chinese': 'zh-Hant',
#     'Czech': 'cs',
#     'Danish': 'da',
#     'Finnish': 'fi',
#     'Canadian French': 'fr-ca',
#     'Indonesian': 'id',
#     'Norwegian': 'nb-NO',
#     'Russian': 'ru',
#     'Thai': 'th',
#     'Turkish': 'tr'
# }
 
# language=Dict[short_language]
# st.write("[Click here for the list of languages that are available](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support)")
# count+=1
    
short_languages = st.multiselect("Select the target languages for translation", 
                                  ["English", "French", "German", "Vietnamese", 
                                   "Chinese(Simplified)", "Dutch", "Italian", 
                                   "Japanese", "Korean", "Polish", 
                                   "Portuguese(Brazil)", "Portuguese(Portugal)", 
                                   "Slovak", "Spanish", "Swedish", "Traditional Chinese", "Czech", "Danish", "Finnish", "Canadian French", "Indonesian", "Norwegian", "Russian", "Thai", "Turkish"], key=count)

Dict = {'English': 'en', 'French': 'fr', 'German': 'de', 'Vietnamese': 'vi', 
        'Chinese(Simplified)': 'zh-Hans', 'Dutch': 'nl', 'Italian': 'it', 
        'Japanese': 'ja', 'Korean': 'ko', 'Polish': 'pl', 
        'Portuguese(Brazil)': 'pt', 'Portuguese(Portugal)': 'pt-pt', 
        'Slovak': 'sk', 'Spanish': 'es', 'Swedish': 'sv', 'Traditional Chinese': 'zh-Hant', 'Czech': 'cs', 'Danish': 'da', 'Finnish': 'fi', 'Canadian French': 'fr-ca', 'Indonesian': 'id', 'Norwegian': 'nb-NO', 'Russian': 'ru', 'Thai': 'th', 'Turkish': 'tr'}


# Get the list of multiple languages in the form of language code from dictionary and store in languages
languages = [Dict[lang] for lang in short_languages]
print ("Multiple Languages selected are...", languages)

st.write("[Click here for the list of languages that are available](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support)")

###
count += 1

#DocTrans_Local2Blob.store2metadata()
#get the time stamp
timestamp = time.time()
dt_object = datetime.fromtimestamp(timestamp)
print("Corresponding Datetime:", dt_object)
 
st.write("Click here to translate")

#Start to execute the below code once Translate button is clicked
if st.button("Translate"):
    if uploaded_file is not None:

        #Define the uploaded file & Filename to reuse in the next for loop iterations 
        file_content = uploaded_file.read()
        filename = uploaded_file.name
        
        for language_name in languages:
            print("language_name..", language_name)
                              
            if language_name is not None:
                
                #start the progress bar
                progress_bar = st.progress(0)

                # Splits filename into root and extension
                nameText = os.path.splitext(filename)

                # Add language name in between the filename and extension  
                fileText = nameText[0] + "-" + language_name + nameText[1]
                
                # Get the file Size
                filesize = len(file_content)
                filesize = filesize/1024
                print("The file size of", filename, "is", filesize, "bytes")

                # Send the Meta data details to store 
                DocTrans_Local2Blob.store2metadata(username, nameText[0], nameText[1], short_languages, dt_object, filesize)
                print(fileText)

                progress_bar.progress(0.10)

                # Send the uploaded file to source container
                DocTrans_Local2Blob.LocalToBlob(file_content, filename)

                progress_bar.progress(0.40)

                # Translate the Source file
                DocTrans_Local2Blob.Translate(language_name)
                progress_bar.progress(0.60)

                # Get the translated content to send it to local system
                content = DocTrans_Local2Blob.BlobToLocal()
                progress_bar.progress(0.80)

                if content is not None:  # Check if content is not None
                    DocTrans_Local2Blob.targetcontainer2targetrepository(fileText)

                    # Save the translated content to a temporary file
                    with open(fileText, "wb") as f:
                        f.write(content)

                    progress_bar.progress(0.90)

                    # Display a link to download the translated file
                    st.markdown("### Download Translated Document.." + language_name)
                    # print(language_name)
                    with open(fileText, "rb") as f:
                        pdf_b64 = base64.b64encode(f.read()).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{pdf_b64}" download="{fileText}">Click here to download</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    progress_bar.progress(100)

                    # Remove the temporary file after displaying the download link
                    os.remove(fileText)  # Use fileText to remove the temporary file
