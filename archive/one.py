import requests as r


# login fail
login_url = "https://ceo.baemin.com/web/login"

data = {
  "id": "klm1144",
  "password":"aa1144aa",
  "token": '03AGdBq25r1IwHJpBJg-jrtN_qxiOZzGMhjdZv7lH2ckJvaHV_qekrLZsrfyZ88UpOINhsDMdm0LloxvAyej8EWK1Pk1enSWGYkaaws0cd3zdw4VlBZGxTPF_ukxoQyWHkK6dKWq4jqFLngbcyon-zfct4CpKid87oIxyA3Edcl_W5Iq8XRNlaf8KHny675eN-D177CtR6KOHFlQakxSxCy1y3ccdBFPn-m3QH0FV4UCzgTY7edU8uQwXkICa6bBH8Yo7uJQMNdy51QTGEinlDqQSmKk_VniJTWtVlBPj06LyAuGW2dtjP0HPGPchm45GYx3-3XTFP-Ng5ifgxlksFAr2g5Pmggt-wfMEzl0w0QVTWJgHnew_yUN_MkmQPwD9hZg2UWBDBqpyBhcQzygLKBz7f2kO-FX3UVNTOFsb0lHNfi_oK-w27hn8'
}
res = r.post(url=login_url, data=data)
print("headers ==", res.headers)
print("cookies ==", res.cookies)


# req data
# "cookie": {'domain': 'ceo.baemin.com', 'httpOnly': False, 'name': '_l_s_id', 'path': '/', 'secure': False, 'value': 'f6fef4c9-db63-49a5-b522-d0a03f2d5f17'}, {'domain': 'ceo.baemin.com', 'expiry': 7912040816, 'httpOnly': False, 'name': 'wcs_bt', 'path': '/', 'secure': False, 'value': '642c55d33b747:1604840816'}, {'domain': '.ceo.baemin.com', 'expiry': 1607432816, 'httpOnly': False, 'name': 'bsgid', 'path': '/', 'secure': False, 'value': '9e870139-6a63-458e-9723-2531f5188adf'},
url = 'https://ceo.baemin.com/v1/orders'
headers = {  
  "cookie": 'bsgid=56a7caf7-6bd3-4144-8fef-ca30dc8e0cd5;  XSRF-TOKEN=724696b0-3b70-4f7c-af5b-4e5f02b267b4; x-s3-request="baemin-imr|AKIAXKIN6VU2IWQQR6SL|20201108|jsKQ34ZeF4bQ15yezc+JRDg6WRKmfU5oTFved24SiYw="; _gat=1; _gat_UA-23009103-53=1; passwordConfirmed=false; _ceo_v2_gk_sid=3ed732c9-39d3-4f43-a98b-ea34f75f594f; wcs_bt=642c55d33b747:1604841169',
  } 

# cookies = {
#   'session_id': '347b72f037ab734174a72d3ea703c0e5'
# } 

param = {
"__ts": "1604822990197",
"sort": "AD_CAMPAIGN_ID",
"shopNo": "" ,
"adInventoryKey": "",
"purchaseType": "",
"orderStatus": "CLOSED",
"startDate": "2020-11-01",
"endDate": "2020-11-07",
"offset": "0"
}

res = r.get(url, headers=headers, params=param)

data = res.json()['data']["histories"]
len(data)