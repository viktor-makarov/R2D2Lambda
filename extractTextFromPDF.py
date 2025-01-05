import http.client
import urllib.parse
from io import BytesIO
import os
import json
import PyPDF2


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

def extracttextfrompdf(pdf_stream):

    text = ''
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extractTextFromPDF(event, context):
  
    url = event["file_url"]

    
    try:
        filestream = download_file(url)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {"error":'Could not fetch the file by url provided',"success":0}
        }

    try:
        text = extracttextfrompdf(filestream)
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
    result = extractTextFromPDF(event,"")

    return result
 
event = {"file_url":"https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/text_pdf.pdf"
}


 
if __name__ == "__main__":
    result = main(event, '')
    print(result)