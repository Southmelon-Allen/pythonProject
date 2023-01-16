import requests
from requests.auth import HTTPDigestAuth

import json

# Replace with the correct URL
pk="SVRhtVre-47Lqj5Tc"

url = "https://api.seniverse.com/v3/weather/now.json?key=SVRhtVre-47Lqj5Tc&location=hangzhou&language=zh-Hans&unit=c"
#url="https://restapi.amap.com/v3/geocode/geo?address=杭州市余杭区西溪堂商务中心7幢&key=6a3115a8b87e7b0a295401a9a3e8b373"


# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime

myResponse = requests.get(url)
print(myResponse.text)