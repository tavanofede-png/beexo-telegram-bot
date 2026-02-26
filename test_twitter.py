import httpx
import re
import json

r = httpx.get('https://syndication.twitter.com/srv/timeline-profile/screen-name/beexowallet', follow_redirects=True, timeout=10)
# Match __NEXT_DATA__ script
m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', r.text)
if m:
    data = json.loads(m.group(1))
    entries = data.get("props", {}).get("pageProps", {}).get("timeline", {}).get("entries", [])
    for e in entries:
        tweet = e.get("content", {}).get("tweet", {})
        if tweet:
            tid = tweet.get("id_str")
            text = tweet.get("text")
            print(f"ID: {tid}")
            print(f"TEXT: {text}")
            print("---")
else:
    print("NO DATA FOUND")
