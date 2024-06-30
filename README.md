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

The backend is also built using Flask and handles incoming requests from the frontend. It uses a machine learning model (Decision Tree Classifier) to predict password strength based on various features like length, character variety, and entropy.

#### Key Features:
- Password strength prediction using a trained model.
- REST API endpoint `/predict` that receives password data and returns strength assessment.
- Training the model on startup using data from `passwords.txt`.

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

#### Application logging:

- Aplication handles logging of frontend and backend.
- Logs are created and dumped into logs/ directory:

`./logs/frontend.txt`

`./logs/backend.txt`