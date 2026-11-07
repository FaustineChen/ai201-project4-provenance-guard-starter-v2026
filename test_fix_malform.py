import requests
url = "http://127.0.0.1:9000/submit"
print(requests.post(url, json={"text": "a", "creator_id": "attacker_MF02"}).status_code)   # expect 400
print(requests.post(url, json=["text", "creator_id"]).status_code)                         # expect 400