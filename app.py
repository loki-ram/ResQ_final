from flask import Flask, render_template
from volunteer import volunteer_bp
import os
from forum import posts
from forum import forum_bp 

app = Flask(__name__)
app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
app.register_blueprint(forum_bp, url_prefix='/forum')  # Register the forum Blueprint

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Chatbot Page
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Disaster Updates Page
@app.route('/disaster')
def disaster():
    return render_template('alert.html')


# Preparedness Tools Page
@app.route('/preparedness')
def preparedness():
    return render_template('preparednesstools.html')





#Help resource allocator
@app.route('/resource')
def resource():
    return render_template('resource.html')

if __name__ == "__main__":
    app.run(debug=True)
