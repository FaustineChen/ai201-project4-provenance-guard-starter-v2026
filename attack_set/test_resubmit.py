import requests

url = "http://127.0.0.1:9000/submit"

r = requests.post(url, data="text=hello&creator_id=attacker_RQ10",
                  headers={"Content-Type": "application/x-www-form-urlencoded"})
print("RQ10", r.status_code, r.text)

r = requests.post(url, data='{"text": "Real writing.", "creator_id": "attacker_RQ11"}',
                  headers={"Content-Type": "text/plain"})
print("RQ11", r.status_code, r.text)