from flask import Flask

app = Flask(__name__)
    
@app.route('/')
def home():
#     count = 0
#     while True:
#         print 
#         count+=1
#         time.sleep(1)
#         count+=1
    return ('Hello, World! ')

@app.route('/about')
def about():
    return 'About'
