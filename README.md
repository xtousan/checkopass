# Checkopass Documentation

## Overview
This documentation outlines the functionality and management of a password strength assessment application. The frontend is a web interface where users can input passwords to check their strength. The backend handles data processing and prediction logic, assessing the strength of passwords based on certain criteria.

## Components

### Frontend (`frontend.py`)

The frontend is built with Flask and serves a simple web form where users can enter passwords to evaluate their strength. It communicates with the backend via API to get the strength assessment.

#### Key Features:
- Web form for submitting passwords.
- Displays password strength as returned by the backend.
- Error handling for backend communication issues.

### Backend (`backend.py`)

#### Overview
The backend of the application is built using the Flask framework, designed to handle HTTP requests from the frontend. It is primarily responsible for evaluating the strength of passwords based on various criteria and using a machine learning model to aid in this determination.

#### Key Features:
- Password strength prediction using a trained model.
- REST API endpoint `/predict` that receives password data and returns strength assessment.
- Training the model on startup using data from `passwords.txt`.

#### Functionality
- **Password Validation**: The backend uses several functions to check the strength of a password. These include checks for minimum length,  presence of upper and lower case letters, digits, and the calculation of password entropy.
- **Machine Learning Model**: A Decision Tree Classifier is employed to predict password strength. This model is trained on a dataset of passwords, where each password is labeled as strong or weak based on predefined criteria.
- **Feature Extraction**: The system extracts features such as password length, the count of uppercase letters, lowercase letters, and digits, alongside entropy values to form a feature set that the Decision Tree Classifier uses.
- **Common Pattern Detection**: The application identifies and filters out common patterns or substrings within passwords that appear frequently across the dataset, classifying passwords containing these as weak.
- **REST API**: A RESTful API endpoint (`/predict`) is provided to receive password data in JSON format and respond with an evaluation of password strength.

#### Machine Learning Logic
- **Training**: The backend initializes by loading a dataset of passwords from a file and identifying common patterns. The Decision Tree Classifier is then trained with features extracted from these passwords, incorporating both numerical and entropy-based features.
- **Prediction**: For incoming password validation requests, the backend extracts features from the provided password, checks it against common patterns, and uses the trained model to classify the password as strong or weak.
- **Model Persistence**: The trained model is saved to disk using `joblib`, allowing for model reuse without retraining for every server restart.

#### Security Note
As the backend handles sensitive information (passwords), it is crucial to ensure that all data is handled securely, especially in production environments. Ensure that communications are encrypted, and consider implementing rate limiting to prevent abuse of the API.

## Installation

1. Ensure Python and Flask are installed.
2. Clone the repository and navigate into the project directory.

```bash
git clone [repository-url]
cd [project-directory]
```

## Running application

1. Run dedicated script

```bash
bash checkopass.sh start
```
2. Stop or restart the application if necessary

```bash
bash checkopass.sh stop
bash checkopass.sh restart
```
3. Interact with the application in your browser by reaching [http://localhost:8080](http://localhost:8080)

#### Application logging:

- Aplication handles logging of frontend and backend.
- Logs are created and dumped into logs/ directory:

`./logs/frontend.txt`

`./logs/backend.txt`