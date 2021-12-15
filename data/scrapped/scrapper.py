import json
import time
import requests

per_page = 100
pages = 100
i = 0
cred = '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'

while pages != 0:
    r = requests.get(
        "https://api.github.com/events", 
        params={"per_page": per_page, "page": 1},
        headers={"Accept":"application/vnd.github.v3+json", "Authorization": "token {}".format(cred),}
    )
    i += 1
    if r.status_code == 200:
        with open('data/scrapped2.txt', 'a') as f:
            for event in r.json():
                f.write(json.dumps(event) + '\n')
        pages -= 1
    else:
        print(r.status_code)
        print(r.json())
    time.sleep(8)
    print(pages)