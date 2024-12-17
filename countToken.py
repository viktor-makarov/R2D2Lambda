import json
from datetime import datetime
import time
import tiktoken

def num_tokens_from_text(text, model="gpt-4o"):

    """Return the number of tokens used by a list of message."""
    try:
        encoding_start_time = time.time()
        enc = tiktoken.encoding_for_model(model)
        encoding_end_time = time.time() 
    except KeyError:
        enc = tiktoken.get_encoding("o200k_base")    

    encoding_time = encoding_end_time - encoding_start_time   
    
    return len(enc.encode(text)),encoding_time
    

def num_tokens_from_message(text, model="gpt-4o"):
    
    """Return the number of tokens used by a list of message."""

    try:
        print(datetime.now())
        encoding = tiktoken.encoding_for_model(model)
        print(datetime.now())
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")
        
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4o"
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(text, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(text, model="gpt-4o")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}."""
        )


def convertToObject(value):
    if isinstance(value, dict):
        return value
    elif isinstance(value, str):
        return json.loads(value)
    else:
        raise NotImplementedError(
            f"""Value "{value}" neither a JSON object nor a string"""
        )


def countTokenInTextRouter(event, context):

    requestObj = convertToObject(event)

    try:
        if not requestObj.get("text") is None :
            text = requestObj["text"]
        else:
            return {
                'statusCode': 400,
                'body': "text field is missing in the request"
            }
            
        if not requestObj.get("model") is None:
            model = requestObj["model"]
        else:
            return {
                'statusCode': 400,
                'body': "model field is missing in the request"
            }
        
        try:
            tokens_count,encoding_time_sec = num_tokens_from_text(text,model)
            return {
                'statusCode': 200,
                'body': {"tokens_count":tokens_count,"encoding_time_sec":encoding_time_sec}
            }
        except NotImplementedError:
            return {
                'statusCode': 500,
                'body': NotImplementedError
            }
    except Exception as err:
        print(err)
        return {
                'statusCode': 500,
                'body': err
            }