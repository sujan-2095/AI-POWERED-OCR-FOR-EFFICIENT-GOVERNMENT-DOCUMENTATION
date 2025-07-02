README - AI Powered OCR for Efficient Government Documentation

📌 Project Overview

This project presents an AI-powered Optical Character Recognition (OCR) system specially designed for recognizing handwritten Tamil characters. It addresses challenges in digitizing regional language documents, particularly for government use, by utilizing Convolutional Neural Networks (CNN) trained on the uTHCD dataset. The solution is deployed as a web application with a user-friendly interface built using Flask.

🎯 Objectives

- Recognize handwritten Tamil characters with high accuracy
- Digitize government documents and historical manuscripts
- Provide real-time OCR through a lightweight web application
- Preserve linguistic heritage through digitization
  
🛠️ Tech Stack

Layer	Technology
Frontend	HTML, CSS, JavaScript, Bootstrap
Backend	Python (Flask)
OCR Engine	CNN (PyTorch)
Database	SQLite
Libraries	OpenCV, PIL, SQLAlchemy

🔄 OCR Workflow Modules

1. Document Image Acquisition
Handles image upload and preprocessing for various formats (.jpg, .png, .bmp).
2. Image Preprocessing
Applies grayscale conversion, noise removal, resizing, and normalization.
3. Text Detection & Segmentation
Detects and isolates text regions using EAST or CTPN.
4. OCR Module
Uses CNN for Tamil character recognition, trained on the uTHCD dataset.
5. Post-OCR Correction
Corrects spelling, normalizes data, and applies regex-based validation.
6. Data Structuring
Formats results into structured data (JSON, XML, CSV).
7. Visualization & Reporting
Presents OCR outputs and performance analytics on a web interface.

📊 Model Performance

The CNN model achieved:
- Training Accuracy: ~98%
- Validation Accuracy: ~95%
- Test Accuracy: ~94%

Misclassifications were primarily among visually similar characters. Preprocessing played a significant role in improving performance.

⚙️ How to Run the Project

1. Clone the repository:
   git clone https://github.com/<your-username>/Tamil-OCR-System.git
   cd Tamil-OCR-System

2. Create virtual environment and activate:
   python -m venv venv
   source venv/bin/activate  (or venv\Scripts\activate for Windows)

3. Install dependencies:
   pip install -r requirements.txt

4. Run the Flask app:
   python main.py

5. Open in browser:
   http://localhost:5000

📂 Dataset Used

The system is trained on the uTHCD (Unconstrained Tamil Handwritten Character Dataset) comprising 91,000 samples across 156 Tamil character classes.

📚 References

- uTHCD Dataset: https://arxiv.org/abs/2103.07676
- TensorFlow & Keras: https://www.tensorflow.org
- Flask: https://flask.palletsprojects.com
- OpenCV: https://docs.opencv.org
- Related papers from ResearchGate, CVIP, and Springer
