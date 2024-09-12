# Algeria Fire Detection Prediction Model

In this project, I experimented with the step-by-step implementation of an ML project lifecycle. It involves data cleaning, exploratory data analysis (EDA), feature engineering, model training, and hyperparameter tuning. After completing the machine learning part, I developed a user interface using Flask and hosted the project on GitHub.

The machine learning models I worked with include Linear Regression, Ridge, Lasso, and ElasticNet. I fine-tuned these models using RidgeCV, LassoCV, and ElasticNetCV, and found that LassoCV gave the best performance.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [API Endpoints](#api-endpoints)
- [Logging](#logging)
- [Error Handling](#error-handling)


## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Flask
- Scikit-learn
- Pandas
- Numpy

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the necessary model and preprocessor files are available in the correct directories:
   - `Preprocessors/KNNImputer.pkl`
   - `Preprocessors/outlier_bounds.json`
   - `Preprocessors/RobustScalar.pkl`
   - `Model/LassoCV.pkl`
3. Run the Flask application:
   ```bash
   python application.py
   ```

## Usage

### API Endpoints

#### 1. `GET /`

Returns the HTML form where users can manually input meteorological data to get predictions.

#### 2. `POST /predict`

Accepts JSON data in the following format to return a prediction:

```json
{
  "region": "0",
  "Temperature": 29,
  "RH": 57,
  "Ws": 18,
  "Rain": 0.0,
  "FFMC": 65.7,
  "DMC": 3.4,
  "ISI": 1.3,
  "Classes": 0
}
```

**Response**:

```json
{
  "prediction": 0.69
}
```

### Example of a POST request using `curl`:

```bash
curl -X POST http://127.0.0.1:5000/predict \\
-H "Content-Type: application/json" \\
-d '{
    "region": "0",
    "Temperature": 39,
    "RH": 57,
    "Ws": 18,
    "Rain": 0.0,
    "FFMC": 65.7,
    "DMC": 3.4,
    "ISI": 1.3,
    "Classes": 0
}'
```

## File Structure

```bash
.
├── application.py        # Flask application
├── dependencies.py       # Contains data transformation and prediction logic
├── Preprocessors/
│   ├── KNNImputer.pkl    # Pre-trained KNN Imputer model
│   ├── outlier_bounds.json  # JSON file containing outlier bounds for preprocessing
│   └── RobustScalar.pkl  # Pre-trained RobustScaler
├── Model/
│   └── LassoCV.pkl       # Pre-trained LassoCV model for prediction
├── static/
│   ├── script.js         # Script file for the HTML page
│   ├── style.css         # Style file for the HTML Page
├── templates/
│   └── index.html        # HTML form for user input
├── app.log               # Log file
├── requirements.txt      # Python dependencies
└── README.md             # This README file
```

## Logging

Logs are generated both to the console and to a rotating log file (`app.log`). The logs capture:
- Info-level messages about predictions and preprocessing.
- Errors encountered during any stage of data processing or prediction.

The log file is rotated once it reaches 10MB, with up to 5 backup files maintained.

## Error Handling

The application has built-in error handling to manage:
- Missing or malformed data in the POST request.
- Errors in loading models or preprocessors.
- Issues in data transformation or prediction.

In case of an error, the API returns a `500` status code along with a descriptive error message.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
