


def execute_python_code(code):
    try:
        exec(code)
    except Exception as e:
        print(f"An error occurred: {e}")

def main(event, context):

    code = event["code"]

    result = execute_python_code(code)

    return result
 
event = {"code":"""
print("Hello, World!")
x = 5
y = 10
print("Sum:", x + y)
"""
}

if __name__ == "__main__":
    main(event, '')

