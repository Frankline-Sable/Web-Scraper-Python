import webbrowser,requests,socket,socketserver
url="http://localhostn/census/default.html"
res=requests.get(url)
print(res.url)

