# 🛡️ ForgeryDetect AI: Enterprise-Grade Document Forensics System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **A Next-Generation AI System for Detecting Document Manipulation with Explainable Visual Forensics.**

## 🚀 Overview
**ForgeryDetect AI** is a state-of-the-art solution designed to combat the rising threat of digital document fraud. Leveraging advanced **Computer Vision** and **Deep Learning** techniques, this system autonomously analyzes uploaded identification documents to detect subtle manipulations, pixel-level artifacts, and inconsistencies invisible to the naked eye.

Unlike black-box models, ForgeryDetect AI prioritizes **Explainability (XAI)**. It not only flags a document as "Forged" or "Authentic" but also provides a dynamic **Neural Activation Heatmap (Grad-CAM)**, pinpointing exactly *where* the manipulation occurred—empowering human reviewers with actionable intelligence.

## ✨ Key Features
*   **🧠 Advanced Deep Learning Core**: Powered by a custom-trained **EfficientNet-B0 (CNN)**, a highly efficient Convolutional Neural Network architecture optimized for feature extraction in synthetic ID documents.
*   **🔍 Explainable AI (XAI)**: Integrated **Grad-CAM (Gradient-weighted Class Activation Mapping)** technology brings transparency to AI decisions, visualizing the specific regions contributing to the forgery probability.
*   **⚡ Real-Time Inference**: High-performance **FastAPI** backend ensures sub-second latency for critical verification workflows.
*   **🎨 Immersive Cyberpunk UI**: A stunning, modern **Streamlit** frontend featuring glassmorphism, laser-scan animations, and responsive design for a premium user experience.
*   **🏗️ Microservices Architecture**: Decoupled Client-Server architecture allows for independent scaling of the inference engine and the user interface.
*   **🔒 Privacy-First Design**: Local processing capabilities ensure sensitive document data never needs to leave the secure perimeter (when deployed on-prem).

## 🛠️ Technology Stack
*   **Model**: PyTorch, EfficientNet-B0 (CNN)
*   **Forensics**: Grad-CAM, OpenCV, NumPy
*   **Backend API**: FastAPI, Uvicorn
*   **Frontend**: Streamlit, Python-Lottie (Animations)
*   **Deployment**: Docker Containers

## 📊 Performance Metrics
The system was trained and validated on the **FantasyID** dataset (a specialized synthetic dataset for ID forgery research):
*   **Accuracy**: 91.1%
*   **Precision**: 94.1%
*   **Recall**: 94.9%
*   **F1 Score**: 94.5%

## 💻 Installation & Setup

### Prerequisites
*   Python 3.9+
*   Git

### Quick Start
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Abhinash200/Forgery-Detect-ai.git
    cd Forgery-Detect-ai
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the System**
    You need to run both the Backend and Frontend terminals.

    **Terminal 1 (Backend API):**
    ```bash
    python backend_api.py
    ```

    **Terminal 2 (Frontend UI):**
    ```bash
    streamlit run frontend_streamlit/app.py
    ```

4.  **Access the App**
    Open your browser and navigate to `http://localhost:8501`.

## 📸 Screenshots
*(This project features a high-fidelity UI with real-time feedback loops and visual indicators for security status)*

## 🔮 Future Roadmap
*   **Multimodal Analysis**: Integrating OCR (Optical Character Recognition) to cross-verify text data against visual consistency.
*   **Blockchain Ledger**: Immutable logging of verification results for audit trails.
*   **Edge Deployment**: Optimizing the model (Quantization) for running on mobile devices/edge nodes.

## 🤝 Contribution
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Abhinash200/Forgery-Detect-ai/issues).

---
*Built with ❤️ by Abhinash*
