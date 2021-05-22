import requests
r = requests.Session()
response = r.get("https://api.telegram.org/bot1856808272:AAHGG2LcUL1dR27CFF6xbrYFMg4XLm-jfBM/sendMessage?chat_id=@blr_vacify&text=This is a test message sent using python script")
