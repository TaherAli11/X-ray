#  Binary File Malware Detection System

This system demonstrates the integration of cybersecurity and deep learning by transforming files of any type, though this project specifically focuses on images due to their higher prevalence compared to other file types into visual representations that a neural network can interpret. This approach introduces a novel and scalable method for malware detection.

This version is designed for clarity, extensibility, and performance, following the best software engineering principles.

---

##  Table of Contents

1. [Overview](#-overview)
2. [Scientific Background](#-scientific-background)
3. [System Architecture](#-system-architecture)
4. [Core Components](#-core-components)
5. [Workflow & Data Flow](#-workflow--data-flow)
6. [Installation & Setup](#-installation--setup)
7. [Running the Application](#-running-the-application)
8. [Model Description](#-model-description)
9. [Future Improvements](#-future-improvements)

---

##  Overview

This project provides a **backend service** that performs the following key tasks:

1. **Accepts a binary or image file upload** via REST API.
2. **Converts binary data into a grayscale image** (a “binary visualization”) using statistical mapping.
3. **Analyzes the resulting image** using a trained deep learning model to predict whether the file represents **malicious (malware)** or **benign** software behavior.
4. **Returns a prediction result**, including the malware classification and the generated visualization image.

This backend is built using:
-  **FastAPI** for the web server (asynchronous, modern Python API framework),
-  **TensorFlow/Keras** for deep learning inference,
-  **Pillow (PIL)** for image generation and manipulation,
-  **Clean Architecture + SOLID principles** for maintainability and scalability.

---

##  Scientific Background

Binary visualization of executables or binary files is an emerging technique in malware analysis.  
The main hypothesis is that **binary structure encodes information about behavior**, which can be **visually represented** and analyzed via image processing.

###  Methodology

1. **Binary Conversion:**
   Each byte (0–255) is treated as an intensity value and used to construct a 2D **byte transition map**:
   \[
   M[x][y] = \text{count of transitions from byte } x \text{ to byte } y
   \]
   This 2D matrix captures byte-frequency relationships (entropy + correlation structure).

2. **Normalization and Visualization:**
   - The logarithm of matrix frequencies is scaled to [0, 255].
   - These values are plotted as pixel intensities in a grayscale image.
   - The resulting image reveals structural patterns in the binary (code density, entropy zones, etc.).

3. **Deep Learning Model:**
   - A **Convolutional Neural Network (CNN)** learns spatial features from these images.
   - The trained model outputs a binary classification:
     - `1 → Malware not detected (benign)`
     - `0 → Malware detected`

This combination of **byte-level statistical visualization** and **image-based classification** allows for **language-agnostic malware detection** — independent of file extension or obfuscation techniques.

---

##  System Architecture

The refactored project follows **Clean Architecture + SOLID principles**:

```bash
backend/
│
├── app/
│ ├── main.py # FastAPI entry point
│ ├── routes/
│ │ └── upload_routes.py # REST API endpoint for upload
│ ├── services/
│ │ ├── file_service.py # File validation & saving
│ │ ├── image_service.py # Binary → Image visualization
│ │ └── model_service.py # Deep learning inference
│ ├── core/
│ │ ├── config.py # Constants & paths
│ │ └── exceptions.py # todo
│ └── utils/
│ └── logger.py # todo
│
│─── models/
│   └── model.h5 # Pretrained Keras malware detection model
│
│─── after_convert/              # Generated visualizations
└─── images/                     # Uploaded files


```


###  Key Architectural Traits

- **SRP (Single Responsibility):**  
  Each service class does exactly one thing (File handling, Image creation, or Model inference).
- **Dependency Inversion:**  
  API routes depend on abstractions (services), not low-level implementations.
- **Modularity:**  
  Easy to replace or upgrade the model or visualization algorithm independently.
- **Testability:**  
  Each service is independently testable (unit + integration testing).

---

##  Core Components

| Component | Responsibility | Input | Output |
|------------|----------------|--------|---------|
| `FileService` | Validates and stores uploaded files | UploadedFile | Saved path |
| `BinaryVisualizer` | Converts binary → grayscale image |  file | PNG image |
| `MalwareDetectionModel` | Predicts malware probability | Image path |  result |
| `FastAPI Routes` | Exposes REST endpoints | HTTP Request | JSON Response |

---

##  Workflow & Data Flow

1. **Client uploads file** (`/upload-image` endpoint).
2. **FileService**:
   - Validates MIME type and size.
   - Saves file securely.
3. **BinaryVisualizer**:
   - Reads the binary byte stream.
   - Constructs a 256×256 transition matrix.
   - Applies logarithmic normalization.
   - Saves image to `/after_convert/`.
4. **MalwareDetectionModel**:
   - Loads pretrained CNN model.
   - Normalizes image input (0–1 range).
   - Predicts class probabilities.
5. **API Response**:
   - Returns classification (`Malware Detected / Not Detected`).
   - Provides generated visualization path.

---

##  Installation & Setup

### Prerequisites

- Python 3.10+  
- `pip` package manager  
- (optional) virtualenv for isolated environment

### 1 Clone the Repository

```bash
git clone https://github.com/yourusername/malware-visualizer-api.git
cd malware-visualizer-api/backend


```


### 2 Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

```


### 3 Install Dependencies
```bash
pip install -r requirements.txt

```

### 4 Running the Application

```bash

uvicorn app.main:app --reload

```

##  Model Description



The model (model.h5) is a Convolutional Neural Network (CNN) trained on images generated from binary files.
### Architecture Overview

- Input layer: 256×256 RGB image
 
- Convolutional layers: extract local byte-structure patterns

- Pooling layers: reduce dimensionality

- Dense layers: aggregate learned representations

- Output: Binary classification (Malware / Benign)

- Training was performed using categorical cross-entropy loss and Adam optimizer.



##  Future Improvements

| Category                 |  Enhancement                                                  | Description                        |
| ------------------------ | ---------------------------------------------------------------------- | ---------------------------------- |
|  **Model**             | Integrate more advanced CNN architectures (e.g., ResNet, EfficientNet) | Improve detection accuracy         |
|  **Async Performance** | Use `aiofiles` for non-blocking file I/O                               | Improve concurrency in FastAPI     |
|  **Logging**           | Centralized structured logging (e.g., `structlog`)                     | Easier debugging and observability |
|  **Testing**           | Implement `pytest` unit and integration tests                          | Ensure robustness                       |
|  **Deployment**        | Dockerize and deploy to AWS/GCP                                        | Production scalability             |




