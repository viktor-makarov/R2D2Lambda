import os
import json

def jsontotextandsetenv(jsonpath, envvar_name):
    try:
        # Чтение JSON-файла
        with open(jsonpath, 'r') as f:
            json_content = json.load(f)

        # Преобразование JSON в текст
        json_text = json.dumps(json_content)
        print(json_text)
        # Установка текста в переменную окружения
        os.environ[envvar_name] = json_text
        
        print(f"Текст из {jsonpath} был успешно добавлен в переменную окружения {envvar_name}.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


file_path = '/home/ec2-user/R2D2LambdaFunctionServerless/my-project-1687854459745-27da374674d5.json'
environmentvariable_name = 'GCP_SERVICE_ACCOUNT_KEY'
jsontotextandsetenv(file_path, environmentvariable_name)
