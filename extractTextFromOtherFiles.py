import http.client
import urllib.parse
from io import BytesIO
from docx import Document
import os
import json

def extracttext(docx_stream):
    doc = Document(docx_stream)
    fullText = []

    for block in doc.element.body.iterchildren():
        tag = block.tag
        if block.tag.endswith('p'):
            print('Paragraph') 
            fullText.append(block.text)
        elif block.tag.endswith('tbl'):
            # Process the table and convert to a string
            table_text = []
            print(dir(block),block.text)
            for text in block.items():
                print("text",text)

                table_text.append('\t'+text)  # Using tab as delimiter
            fullText.append('\n'.join(table_text))

    return '\n'.join(fullText)

def download_file(url):
    # Parse the URL to extract components
    url_parts = urllib.parse.urlparse(url)
    conn = http.client.HTTPSConnection(url_parts.netloc)
    conn.request("GET", url_parts.path)
    response = conn.getresponse()
    
    if response.status != 200:
        raise Exception(f"Failed to download file: {url} {response.status} {response.reason}")

    binaryObject = BytesIO(response.read())
    binaryObject.name = url_parts.path.split('/')[-1]
    
    # Read the response data into a BytesIO object
    return binaryObject

def extracttextfromtxt(txt_stream):
    return txt_stream.read().decode('utf-8')

def extracttextfromtxt(filestream):
    return filestream.read().decode('utf-8')

def extracttextfromdocx(docx_stream):

    doc = Document(docx_stream)
    
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

    doc = Document(docx_stream)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extracttextfromfile(filestream, mime_type):

    if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text = extracttextfromdocx(filestream)
    elif mime_type.startswith('text/') or mime_type == 'application/json':
        text = extracttextfromtxt(filestream)
    else:
        raise ValueError("Unsupported file type")
    return text

def extractTextFromOtherFileRouter(event, context):
  
    url = event["file_url"]
    
    try:
        filestream = download_file(url)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {"error":'Could not fetch the file by url provided',"success":0}
        }
    mime_type  = event["file_mime_type"]

    try:
        text = extracttextfromfile(filestream, mime_type)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {"error":e,"success":0}
        }

    return {
        'statusCode': 200,
        'body': {"text":text,"success":1}
    }
    	
def main(event, context):
    result = extractTextFromOtherFileRouter(event,"")

    return result
 
#event = {"file_url": "https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/test_text2.txt","file_mime_type": "text/plain"}

#event = {"file_url": "https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/test_text.json", "file_mime_type": "application/json"}

event = {
"file_url":"https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/test_doc.docx",
"file_mime_type":"application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

 
if __name__ == "__main__":
    result = main(event, '')
    print(result)