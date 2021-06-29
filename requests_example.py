from pprint import pprint

import requests

# проверяйте с http/https, www и без
url = "https://www.google.ru"
# www - 6072
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}
response = requests.get(url, headers=headers)

print(response)
print(response.status_code)
print("---content-length---")
# print(response.headers['Content-Length'])
# print(len(response.content))
print()
pprint(dict(response.headers))
pprint(response.text)
print()
