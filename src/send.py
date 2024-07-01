# 예시 데이터 업로드 
import requests

url = "http://127.0.0.1:8000/jobs"
data = {
    "subject": "New Job",
    "content": "This is a new job.",
    "create_date": "2023-04-24T12:34:56"  # 날짜 형식은 데이터베이스와 일치해야 함
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Job created successfully!")
else:
    print(f"Error creating job: {response.status_code} - {response.text}")
