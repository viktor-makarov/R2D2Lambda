import io
import sys


def execute_python_code(code):
    
    original_stdout = sys.stdout

    try:
        sys.stdout = io.StringIO()
        exec(code)
        result = {"result":sys.stdout.getvalue(),"success":1}
        sys.stdout = original_stdout
        
    except Exception as e:
        sys.stdout = original_stdout
        result =  {"error":f"An error occurred: {e}","success":0}

    return result

def main(event, context):

    code = event["code"]
    try:
        result = execute_python_code(code)
        if result["success"] == 1:
            return {
                'statusCode': 200,
                'body': result
            }
        else:
            return {
                'statusCode': 500,
                'body': result
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {"error":e,"success":0}
        }
 
event = {"code":"""
print("Hello, World!")
x = 5
y = 10
print("Sum:", x + y)
"""
}

if __name__ == "__main__":
    result = main(event, '')
    print(result)

