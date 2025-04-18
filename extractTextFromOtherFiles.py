import http.client
import urllib.parse
from io import BytesIO
from docx import Document
from docx.oxml.ns import qn


def extracttextFromDocx(docx_stream):

    doc = Document(docx_stream)
    fullText = []

    for block in doc.element.body.iterchildren():
        tag = block.tag
        if block.tag.endswith('p'):
            # Handle paragraphs
            paragraph_text = []
            for run in block.iter(qn('w:r')):
                text_elements = run.findall(qn('w:t'))
                for elem in text_elements:
                    if elem.text:
                        paragraph_text.append(elem.text)

            fullText.append(''.join(paragraph_text))
        elif block.tag.endswith('tbl'):
            # Process the table and convert to a string
            table_text = []
            for row in block.iter(qn('w:tr')):
                row_text = []
                for cell in row.iter(qn('w:tc')):
                    cell_text = []
                    for paragraph in cell.iter(qn('w:p')):
                        para_text = []
                        for run in paragraph.iter(qn('w:r')):
                            text_elements = run.findall(qn('w:t'))
                            for elem in text_elements:
                                if elem.text:
                                    para_text.append(elem.text)
                        cell_text.append(''.join(para_text))
                    row_text.append(' | '.join(cell_text))
                table_text.append(' | '.join(row_text))
            fullText.append('\n'.join(table_text))

    return '\n'.join(fullText)


    # Create a Word application object
    word = win32com.client.Dispatch("Word.Application")
    # Open the .doc file
    doc = word.Documents.Open(file_path)
    
    # Extract the text
    text = doc.Content.Text
    
    # Close the document and quit Word
    doc.Close()
    word.Quit()
    
    return text

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

def extracttextfromfile(filestream, mime_type):

    if mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text = extracttextFromDocx(filestream)
    elif mime_type == 'application/msword':
        text = extracttextFromDocx(filestream)
    elif mime_type.startswith('text/') or mime_type == 'application/json':
        text = extracttextfromtxt(filestream)
    else:
        text = "Unsupported file type"
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

#event = {"file_url":"https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/test_doc.docx","file_mime_type":"application/vnd.openxmlformats-officedocument.wordprocessingml.document"}

event = {"file_url":"https://r2d2storagedev.s3.eu-north-1.amazonaws.com/incoming_files/test.doc","file_mime_type":"application/msword"}
 
if __name__ == "__main__":
    result = main(event, '')
    print(result)