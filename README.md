# Multisensor Failure Detection Project

This repository contains code and models for detecting failures based on multiple sensor inputs, including temperature, vibration, RPM, and audio data. The project processes these features in real-time to identify anomalies or faults, supporting predictive maintenance and operational monitoring.

## Repository Structure

### 1. `analysis code` Folder

Contains Jupyter notebooks for analyzing and processing data from various sensors, as well as evaluating model performance for failure detection.

- **`audio_processing.ipynb`**: Processes audio data, extracting relevant features to support failure detection. This includes signal transformations and feature visualization.
- **`Data_Analysis.ipynb`**: Analyzes the structure and distribution of multisensor data (temperature, vibration, RPM, audio), identifying trends or anomalies that may indicate potential failures.
- **`Model_Analysis.ipynb`**: Evaluates the failure detection model's performance using metrics such as accuracy, precision, and recall on the processed data from all sensors.

### 2. `audio.py`

Contains functions for audio processing, including filtering and feature extraction, which are used to detect audio anomalies as part of the failure detection process:
- **`filter_audio`**: Applies a band-pass filter to the audio signal, enhancing relevant frequency components.
- **`audio_features`**: Extracts key audio features that contribute to identifying faults.
- **`record_audio`**: Manages audio recording and stores frames that can later be analyzed for issues.

### 3. `audio_comunication.py`

Manages UDP communication for remote monitoring, enabling real-time transmission of audio and other sensor data (e.g., temperature, vibration, RPM) between a client and server. It supports:
- Commands to start and stop data recording.
- Processing and sending extracted audio features over the network.
- Real-time communication over a specified IP and port.

### 4. `model.joblib`

A pre-trained failure detection model that uses features from temperature, vibration (accelerometer), RPM, and audio data to identify potential issues. This model analyzes incoming data in real-time or batch mode, assessing whether the inputs indicate a fault.

### 5. `rasp_code`

This script is designed for edge devices like a Raspberry Pi, where it reads data from sensors (temperature, accelerometer for vibration, RPM, and microphone for audio) and uses the `model.joblib` file to perform real-time failure detection.

- **Functionality**:
  - Initializes and reads from sensors connected to the Raspberry Pi.
  - Processes and normalizes sensor data.
  - Applies the pre-trained failure detection model to identify potential faults.
  - Can trigger alerts or send data to a remote server based on detection results.

### 6. `sensors_tests` Folder

This folder contains various Python scripts for testing individual sensors and capturing data, including temperature, RPM, accelerometer (vibration), and audio. These scripts are primarily used to validate sensor connectivity and data collection.

- **`acelerometer_test.py`**: Reads accelerometer and gyroscope data from an MPU6050 sensor, including measurements for temperature and acceleration along the X, Y, and Z axes.
- **`arduino_reading.py`**: Communicates with an Arduino via serial to read sensor data at regular intervals. The Arduino connection is configured to read data from `/dev/ttyUSB1` at a 115200 baud rate.
- **`IRsensor.py`**: Uses an infrared (IR) sensor to detect the presence of nearby objects, toggling an LED based on proximity. This script is designed for use with Raspberry Pi GPIO pins.
- **`measure_rpm.py`**: Calculates RPM (rotations per minute) by counting interruptions detected by an IR sensor on a spinning wheel with defined slots. The script calculates RPM based on the time interval between slot counts.
- **`motor_test.py`**: Controls a motor via PWM (pulse-width modulation) to adjust duty cycle, allowing for testing different motor speeds. Input values range from 0 to 100, representing the duty cycle percentage.
- **`sensors_connectivity.py`**: A comprehensive script that combines multiple sensor readings, including RPM, temperature (using an MLX90614 infrared thermometer), and accelerometer data. This class-based script sets up GPIO configurations, reads data from each sensor, and manages the motor using a PWM signal.
- **`temperature_test.py`**: Reads ambient and object temperatures using an MLX90614 sensor, providing a simple test of the temperature sensor’s accuracy and connectivity.
- **`test.py`**: Demonstrates an example of UDP communication using a client-server setup, transmitting simple messages to test network connectivity.
- **`test_audio.py`**: Records audio data received via serial from an Arduino, normalizes it, and saves it as a `.wav` file. Includes plots of raw and normalized audio data for analysis.

These scripts serve as unit tests for individual components, ensuring each sensor and data collection method functions correctly before integrating into the main failure detection system.

## Usage

1. **Install Dependencies**:
   Ensure you have Python 3.x, Jupyter Notebook, and the necessary libraries installed:
   ```bash
   pip install -r requirements.txt


### Key Dependencies

- `jupyter`
- `numpy`
- `scipy`
- `matplotlib`
- `librosa` (for audio processing)
- `pyaudio` (for audio input)
- `socket` and `pickle` (for communication)
- Sensor-specific libraries for temperature, accelerometer, and RPM reading

### Run the Notebooks

- Navigate to the `analysis code` folder and execute each notebook sequentially:
  - **`audio_processing.ipynb`**: Extract audio features for failure detection.
  - **`Data_Analysis.ipynb`**: Analyze multisensor data, looking for patterns that may indicate faults.
  - **`Model_Analysis.ipynb`**: Evaluate the model’s performance on the integrated sensor data.

### Execute Sensor Processing Scripts

- Use `audio.py` to filter, extract features, and record audio data as part of the failure detection process.
- Run `audio_comunication.py` to establish a server-client connection for real-time transmission of audio and other sensor data, allowing remote monitoring for faults.
- Run `rasp_code` on your Raspberry Pi to read sensor data and perform real-time failure detection using the trained model.

### Dataset

Prepare a custom dataset that includes:

- **Temperature Readings**: Capturing variations that may indicate overheating or component wear.
- **Vibration Data**: Collected via an accelerometer, indicating abnormal movement or mechanical issues.
- **RPM Data**: Reflecting speed variations that could signal impending failures.
- **Audio Samples**: Including normal and abnormal sounds to support audio-based fault detection.

### Edge Model Deployment

The failure detection model is optimized for edge deployment, enabling real-time monitoring and fault detection directly on devices like the Raspberry Pi. This setup supports rapid response and privacy by keeping data processing on-site.

### Notes

- The audio processing and communication modules may require specific configurations for microphone, accelerometer, and network settings.
- The `rasp_code` script is intended for use on a Raspberry Pi or similar device where sensor data can be collected and processed locally.
- The model file (`model.joblib`) is pre-trained to recognize failure patterns across temperature, vibration, RPM, and audio features; use `Model_Analysis.ipynb` to evaluate its performance on your dataset.

### Output

- Each notebook provides code, explanations, and visualizations for detecting failures based on multisensor data.
- Processing scripts log steps in real-time to support continuous monitoring and fault identification.

