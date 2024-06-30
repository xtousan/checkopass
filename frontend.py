from flask import Flask, render_template, request, jsonify, session
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    password = None
    result = None
    error = None
    password_visible = 'text'  # Default state is visible

    if request.method == 'POST':
        password = request.form.get('password')
        password_visible = request.form.get('password_visible', 'text')
        if password:
            # Backend API call and response handling
            response = requests.post('http://localhost:5000/predict', json={'password': password})
            if response.status_code == 200:
                result = response.json()['strength']
            else:
                error = "Error connecting to the backend."

    return render_template('index.html', password=password, result=result, error=error, password_visible=password_visible)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
