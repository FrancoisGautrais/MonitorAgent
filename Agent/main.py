import requests
import gloabls
import remove.clean
r = requests.get('https://github.com/timeline.json')
print(r.status_code)


