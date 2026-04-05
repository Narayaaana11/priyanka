# Event Prediction Project

This project predicts whether a social-media event is likely to trend based on tweet activity, unique users, retweets, and time span.

## Project Structure

- `backend/app.py`: Flask API that loads the datasets, trains the model on startup, and exposes the `/predict` endpoint.
- `backend/preprocess.py`: Reads both CSV datasets, standardizes the columns, and builds event-level features.
- `backend/model.py`: Trains a `GaussianNB` model with scaled features and returns predictions plus probabilities.
- `frontend/index.html`: User interface for entering event metrics.
- `frontend/script.js`: Sends prediction requests to the backend and renders the result in the UI.
- `frontend/style.css`: Frontend styling.
- `data/twitter_dataset.csv`: Input dataset 1.
- `data/tweets.csv`: Input dataset 2.

## Software Required

Install these on the system before running the project:

- Python 3.11 or newer
- `pip` for Python package installation
- A modern browser such as Chrome, Edge, or Firefox

No virtual environment is required for this project.

## Python Packages Required

The project uses these Python packages:

- `pandas`
- `scikit-learn`
- `flask`
- `flask-cors`
- `numpy`

They are already listed in `requirements.txt`.

## How the Project Works

1. `backend/app.py` starts first.
2. On startup, it loads both CSV files from the `data/` folder.
3. The backend combines the datasets into one dataframe.
4. The model prepares event-level features:
   - tweet count
   - unique users
   - retweet sum
   - time span
   - average retweets
   - user ratio
5. A `GaussianNB` classifier is trained when the backend starts.
6. The frontend collects user inputs and sends them to `http://127.0.0.1:5000/predict`.
7. The backend returns:
   - prediction
   - probability
   - explanations
   - feature importance

## Installation

Open PowerShell in the project root folder and run:

```powershell

python -m pip install --user -r requirements.txt

```

If `python` does not work on the other machine, use:

```powershell

py -m pip install --user -r requirements.txt

```

## Exact Execution Steps

### 1. Open terminal in the project folder

Example:

```powershell

cd C:\path\to\event-prediction

```

### 2. Install packages

```powershell

python -m pip install --user -r requirements.txt

```

### 3. Start the backend server

Run this from the project root:

```powershell

python backend\app.py

```

What happens here:

- Flask starts on `http://127.0.0.1:5000`
- The datasets are loaded automatically
- The model is trained automatically
- Accuracy and sample predictions are printed in the terminal

Wait until you see Flask running before opening the frontend.

### 4. Open the frontend

You have two simple options.

Option A: Open the HTML file directly in a browser

```powershell

start frontend\index.html

```

Option B: Run a simple local frontend server

```powershell

cd frontend

python -m http.server 5500

```

Then open:

```text

http://127.0.0.1:5500

```

Option B is recommended if the browser blocks local file requests.

## Normal Run Flow

1. Start the backend terminal.
2. Open the frontend in the browser.
3. Enter values for:
   - Tweet Count
   - Unique Users
   - Retweet Sum
   - Time Span
4. Click `Run Prediction`.
5. View the result card, confidence score, explanations, and feature importance.
6. Use `Reset` to clear the previous result and enter a new prediction.

## Important Notes for Sharing This Project

- Send the full project folder, including the `data/` folder.
- Do not remove or rename the CSV files.
- The backend must be running before live predictions work.
- If the backend is not running, the frontend falls back to demo mode in `script.js`.
- No Node.js, npm, or frontend package installation is required.

## Common Problems and Fixes

### Problem: `python` command is not recognized

Use:

```powershell

py backend\app.py

```

and

```powershell
py -m pip install --user -r requirements.txt
```

### Problem: `ModuleNotFoundError`

Run the package installation again:

```powershell
python -m pip install --user -r requirements.txt
```

### Problem: Frontend opens but only demo mode appears

Cause:

- The backend server is not running, or
- Flask failed to start

Fix:

- Check the backend terminal for errors
- Make sure Flask is running on `http://127.0.0.1:5000`
- Refresh the browser after the backend starts

### Problem: Port 5000 is already in use

Edit `backend/app.py` and change the Flask port, then also update the fetch URL in `frontend/script.js`.

## Recommended Handover Instructions

If you send this project to another person, also send these short instructions:

1. Extract the project folder.
2. Open PowerShell in the project root.
3. Run `python -m pip install --user -r requirements.txt`
4. Run `python backend\app.py`
5. Open `frontend\index.html` in a browser
6. Keep the backend terminal open while using the frontend

## Quick Start

```powershell

cd C:\path\to\event-prediction

python -m pip install --user -r requirements.txt

python backend\app.py

start frontend\index.html

```



OPEN TERMINAL CTRL+SHIFT+`

BACKEND EXECUTION (Terminal 1):-

cd backend
python app.py

NOTE :- you should run the backend in the terminal before going to the frontend

FRONTEND EXECUTION(Terminal 2):-

cd frontend
python -m http.server 5500

OR ELSE 

you can directly open file explorer
and open the project file and open frontend file you will see a index(HTML File) double click on it you will be redirected to your respective browser 