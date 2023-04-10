from flask import Flask

app = Flask(__name__)

count = 0
    
@app.route('/')
def home():

#     while True:
#         print 
#         count+=1
#         time.sleep(1)
#     count+=1
    return ('Hello, World! ',count)

@app.route('/about')
def about():
    return 'About'
