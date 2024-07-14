# Business Contract Validation

This project aims to compare two business contract PDF files and highlight the differences between them using a Streamlit interface. The differences are highlighted in the output PDF file.

## Features

- Upload two PDF files.
- Highlight differences between the two PDF files.
- Download the highlighted differences PDF.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/BusinessContractValidation.git
    cd BusinessContractValidation
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Configuration
Modify the absolute path in app.py (line 5) to reflect the path of scripts in your environment. 

## Usage (Without docker)

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Upload the two PDF files you want to compare.

4. Click the "Generate Differences PDF" button.

5. Download the highlighted differences PDF.

## Run the Docker Container

The docker image is available at 'https://hub.docker.com/repository/docker/gaurisankar/bcv/general'

1) Build the container 

    ```bash
    docker build -t business-contract-validation .
    ```
2) Run the container

    ```bash
    docker run -p 8501:8501 business-contract-validation
    ```