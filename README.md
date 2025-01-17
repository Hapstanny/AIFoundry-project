# AIFoundryDemo

## Deploy Custom LLM Application to **Azure AI Foundry** as Managed Endpoint with **Tracing & Evaluation**

## Overview
AIFoundryDemo is a demo application for monitoring AI projects using Azure AI Foundry. This project demonstrates how to create, trace, evaluate and custom LLM application in Azure AI Foundry Project


**Broadly below activties were covered** - 
- Created **Custom LLM Application** based on Flask.
- Created **AI Foundry** Managed Online Endpoint
- Deployed Application to Managed Endpoint
- Traced functions in **AI Foundry Project**
- Reviewed Evalution results in **AI Foundry Project** evaluation
- Integrated results in **App Insight Dashboard**

## Prerequisites
- Python 3.8+
- Azure AI Foundry SDK for Python
- Create **Azure AI Foundry** Hub 
- Create **Azure AI Foundry** Project
- Create **Connection Azure AI Services** with Azure Open AI deployments
- Integrate/Update **APP Insight** & **Containter App** resources ID with AI HUB 


## Installation
1. Clone the repository:
    git clone <repository_url>
    cd aifoundrydemo


2. Create a virtual environment:
    python -m venv .venv


3. Activate the virtual environment:
    - On Windows:
        .venv\Scripts\activate

    - On macOS/Linux:
        source .venv/bin/activate

4. Install the required packages:
    pip install -r requirements.txt

## Local Run
1. Set up your Azure credentials and configuration in environment variables or a configuration file.

2. Run the main script:
    python3 app.py

3. Run below to call Chat API
    curl -X POST "http://localhost:5001//chat/products" -H "Content-Type: application/json"  -d '{"query":"Tell me good trekking wear for mount Everest climb","enable-telemetry":"False"}'

4. Run below to call Evalution API
    curl -X GET "http://localhost:5001/chat/evaluations"

## Deployment to Managed Endpoint
The AIFoundryDemo can be deployed to a managed endpoint using the provided Jupyter notebook. Follow these steps:

1. **Navigate to the Deployment Folder**:
    cd deployment

2. **Open the Deployment Notebook**:
    - In the Jupyter interface, open the `ManageEndpointDeployment.ipynb` notebook.

4. **Follow the Notebook Instructions**:
    - Follow the step-by-step instructions in the notebook to configure and deploy your application to the managed endpoint.

## Test the Deployment
Send a request to the deployed endpoint:

    <code>
    import requests, json

    url = "https://<endpoint_name>.azurewebsites.net/score"
    headers = {"Authorization": "Bearer <token>", "Content-Type": "application/json"}
    payload = json.dumps({"query": "Items to carry for Everest expedition"})
    response = requests.post(url, headers=headers, data=payload)
    print(response.json())
    </code>
:

## Processing Screenshots
- **Tracing**

![Alt text](/images/Tracing1.png)

- **AI Insight Dashboard**

![Alt text](/images/AI_Insight_Dashboard.png)

- **Evaluations** 

![Alt text](/images/Evaluations.png)

- **Chat API Run** 

![Alt text](/images/Chat_Product_run.png)

- **Evaluation Run**

![Alt text](/images/Evaluations_run.png)

- **Managed Endpoint**

![Alt text](/images/managed_endpoint.png)

