from flask import Flask

app =  Flask(__name__)

@app.route('/') #http://www.site.com/ -  refers to / after .com
def home():
    return "Hello, World!"

app.run(port=5000)
