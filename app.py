from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import traceback
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS  # For handling cross-origin requests

app = Flask(__name__)

# Allow communication from your frontend (localhost on port 5500)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Load the ML model
model_path = 'crop_prediction_model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Load crop names and prepare LabelEncoder
data = pd.read_csv('V3_crop_environment_data_with_lih_and_advice_with_error.csv')
crop_names = data['Crop Name'].unique().tolist()
label_encoder = LabelEncoder()
label_encoder.fit(crop_names)

# Google Sheets configuration
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name('black-media-386619-0e541c4ee39e.json', scope)
client = gspread.authorize(creds)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1bOPtxYV2xsDtBWfj8EhQniRMEafk6mBUr_DoD9et5is/edit?gid=152194846'
worksheet = client.open_by_url(spreadsheet_url).sheet1

def fetch_last_row():
    """Fetch the last row of data from the Google Sheet."""
    data = worksheet.get_all_values()
    if not data or len(data) < 2:
        return {}
    headers = data[0]
    last_row = data[-1]
    return {headers[i]: last_row[i] for i in range(len(headers))}


@app.route('/', methods=['GET', 'POST'])
def home():
    last_row = get_last_row()  # Fetch the last row from the sheet
    if request.method == 'POST':
        try:
            # Get input values from the form
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            soil_moisture = float(request.form['soil_moisture'])
            light_intensity = float(request.form['light_intensity'])
            crop_name = request.form['crop_name']
            
            # Encode the crop name
            crop_name_encoded = label_encoder.transform([crop_name])[0]
            
            # Create a DataFrame for the input data
            input_data = pd.DataFrame([[temperature, humidity, soil_moisture, light_intensity, crop_name_encoded]],
                                      columns=['Temperature', 'Humidity', 'Soil Moisture', 'Light Intensity', 'Crop Name'])

            # Make prediction
            prediction = model.predict(input_data)
            advice = prediction[0]  # Store the prediction result
            return jsonify({'Advice': advice})
        except Exception as e:
            # Print error details to console
            print("An error occurred:", e)
            traceback.print_exc()
            return jsonify({'error': 'An error occurred. Please try again.'}), 500

    return render_template('index.html', crop_names=crop_names, last_row=last_row)



@app.route('/get_last_row', methods=['GET'])
def get_last_row():
    try:
        last_row_dict = fetch_last_row()
        return jsonify(last_row_dict)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch data from Google Sheets'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse request data
        data = request.json
        print('req data : ',data)
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        soil_moisture = float(data['soil_moisture'])
        light_intensity = float(data['light_intensity'])
        crop_name = data['crop_name']

        # Encode crop name and predict
        crop_name_encoded = label_encoder.transform([crop_name])[0]
        input_data = pd.DataFrame([[temperature, humidity, soil_moisture, light_intensity, crop_name_encoded]],
                                  columns=['Temperature', 'Humidity', 'Soil Moisture', 'Light Intensity', 'Crop Name'])
        prediction = model.predict(input_data)
        advice = prediction[0]
        return jsonify({'advice': advice})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)

