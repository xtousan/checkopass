from flask import Flask, request, jsonify
import logging
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load
import math

app = Flask(__name__)
model = None
common_patterns = []

def password_entropy(password):
    freq = {char: password.count(char) for char in set(password)}
    entropy = -sum((count / len(password)) * math.log2(count / len(password)) for count in freq.values())
    return entropy

def extract_features(passwords):
    return [
        [
            len(p), 
            sum(c.isdigit() for c in p), 
            sum(c.isupper() for c in p), 
            sum(c.islower() for c in p)
        ] for p in passwords
    ]

def find_common_patterns(passwords, threshold=0.0001):
    substrings = {}
    min_length = 4
    for password in passwords:
        for start in range(len(password) - min_length + 1):
            for end in range(start + min_length, len(password) + 1):
                substr = password[start:end].lower()
                substrings[substr] = substrings.get(substr, 0) + 1
    total = len(passwords)
    return [substr for substr, count in substrings.items() if count / total >= threshold]

def is_strong(password, common_patterns):
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if len(password) < 8 or password_entropy(password) < 3:
        return False
    if not (has_upper and has_lower and has_digit):
        return False
    if any(pattern in password.lower() for pattern in common_patterns):
        return False  # Classify as weak if any common pattern is found
    return True

def load_data():
    try:
        with open('passwords.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error("Passwords file does not exist.")
        return []

def train_model(passwords):
    features = extract_features(passwords)
    labels = [int(is_strong(p, common_patterns)) for p in passwords]
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    dump(clf, 'password_model.joblib')
    logging.info(f"Model trained with accuracy: {clf.score(X_test, y_test)}")
    return clf

@app.route('/predict', methods=['POST'])
def predict():
    content = request.json
    password = content.get('password', '')
    if password:
        strength = "Strong" if is_strong(password, common_patterns) else "Weak"
        logging.info(f"Password evaluated: {password} - Strength: {strength}")
        return jsonify({'password': password, 'strength': strength})
    return jsonify({'error': 'No password provided.'}), 400

# Main function starts here
if __name__ == '__main__':
    passwords = load_data()
    common_patterns = find_common_patterns(passwords)
    if passwords:
        model = train_model(passwords)
    app.run(host='0.0.0.0', port=5000, debug=False)
