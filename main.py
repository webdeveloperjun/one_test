import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts")
element = response.json()
first_five = element[:5]
for i in first_five:
    print(i["title"])

response_dict = {
    "title": "Task completed",
    "body": "I have notebook its cool",
    "userId": 2344212
}

new_user = requests.post("https://jsonplaceholder.typicode.com/posts", json=response_dict)
print(new_user.status_code)