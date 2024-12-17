import http.client
import urllib.parse
from io import BytesIO
from docx import Document
import pandas as pd
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

def extracttextfromtxt(txt_stream):
    return txt_stream.read().decode('utf-8')

def extracttextfromdocx(docx_stream):
    doc = Document(docx_stream)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extracttextfromxlsx(xlsx_stream):
    df = pd.read_excel(xlsx_stream)
    dftext = df.to_string(index=False)
    
    return dftext

def extracttextfrompdf(pdf_stream):

    text = ''
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

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

def ocrPDF(filestream):
    return "OCR yе реализован"    

def extracttextfromfile(filestream, mime_type):

    if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text = extracttextfromdocx(filestream)
    elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        text = extracttextfromxlsx(filestream)
    elif mime_type.startswith('text/') or mime_type == 'application/json':
        text = extracttextfromtxt(filestream)
    elif mime_type == 'application/pdf':
        text = extracttextfrompdf(filestream)
        noTextFound = len(text) < 10

        if noTextFound:
            text = ocrPDF(filestream)
        
    elif mime_type == 'image/jpeg':
        text = ocrImage(filestream)
    else:
        raise ValueError("Unsupported file type")
    
    return text

def extractTextFromFileRouter(event, context):
  
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
    result = extractTextFromFileRouter(event,"")

    print("result",result)
 
#event = {"file_url":"https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/5248593849_1893.pdf","file_mime_type":"application/pdf"}

#event = {"file_url": "https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/5248593849_1866.txt", "file_mime_type": "text/plain"}

event = {"file_url":"https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/5248593849_30727.xlsx","file_mime_type":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}

#event = {"file_url": "https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/5248593849_1867.json", "file_mime_type": "application/json"}

#event = {"file_url":"https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/5248593849_1875.docx","file_mime_type":"application/vnd.openxmlformats-officedocument.wordprocessingml.document"}

 
if __name__ == "__main__":
    main(event, '')