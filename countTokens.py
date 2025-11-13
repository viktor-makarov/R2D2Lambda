import json
from datetime import datetime
import time
import tiktoken

def num_tokens_from_text(text, model="gpt-4o"):
    """Return the number of tokens used by a list of message."""
    encoding_start_time = time.time()
    errorMsg = None
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError as e:
        # Log the error to console
        errorMsg = f"Input model '{model}' - {e}"    
        # Try fallback encodings in order of preference
        if "gpt-4" in model:
            enc = tiktoken.get_encoding("o200k_base")
            errorMsg += f" Using o200k_base as fallback."
        elif "gpt-5" in model:
            enc = tiktoken.get_encoding("o200k_base")
            errorMsg += f" Using o200k_base as fallback."
        elif "gpt-3.5" in model:
            enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
            errorMsg += f" Using fallback encoding for gpt-3.5-turbo."
        else:
            # Final fallback
            enc = tiktoken.get_encoding("o200k_base")
            errorMsg += f" Using o200k_base as final fallback."
    finally:
        encoding_end_time = time.time()

    if errorMsg:
        print("Error:",errorMsg)
    encoding_time = round(encoding_end_time - encoding_start_time, 3)
    
    return len(enc.encode(text)), encoding_time, errorMsg
    

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
            tokens_count, encoding_time_sec, error_msg = num_tokens_from_text(text, model)
            response = {
                'tokens_count': tokens_count,
                'encoding_time_sec': encoding_time_sec
            }
            if error_msg:
                response['warning'] = error_msg
            return {
                'statusCode': 200,
                'body': response
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

def main(event, context):
    result = countTokenInTextRouter(event,"")

    return result

event = {
  "text": "test text from AWS",
  "model": "gpt-5.1"
}

if __name__ == "__main__":
    result = main(event, '')
    print(result)