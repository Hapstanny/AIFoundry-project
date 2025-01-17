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
    <code>git clone <repository_url>
    cd aifoundrydemo</code>


2. Create a virtual environment:
    <code>python -m venv .venv</code>


3. Activate the virtual environment:
    - On Windows:
        <code>.venv\Scripts\activate</code>

    - On macOS/Linux:
        <code>source .venv/bin/activate</code>

4. Install the required packages:
    <code>pip install -r requirements.txt</code>

## Local Run
1. Set up your Azure credentials and configuration in environment variables or a configuration file.

2. Run the main script:
    <code>python3 app.py</code>

3. Run below to call Chat API
    <code>curl -X POST "http://localhost:5001//chat/products" -H "Content-Type: application/json"  -d '{"query":"Tell me good trekking wear for mount Everest climb","enable-telemetry":"False"}'</code>

4. Run below to call Evalution API
    <code>curl -X GET "http://localhost:5001/chat/evaluations"</code>

## Deployment to Managed Endpoint
The AIFoundryDemo can be deployed to a managed endpoint using the provided Jupyter notebook. Follow these steps:

1. **Navigate to the Deployment Folder**:
    cd deployment

2. **Open the Deployment Notebook**:
    - In the Jupyter interface, open the `ManageEndpointDeployment.ipynb` notebook.

4. **Follow the Notebook Instructions**:
    - Follow the step-by-step instructions in the notebook to configure and deploy your application to the managed endpoint.

## Test the Deployment
1. **Send a POST request to the deployed endpoint /chat/products**:

<code>
    import requests, json
    from urllib.parse import urlsplit

    url_parts = urlsplit(endpoint.scoring_uri)
    url = url_parts.scheme + "://" + url_parts.netloc

    token = ml_client.online_endpoints.get_keys(name=online_endpoint_name).primary_key
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    payload = json.dumps(
        {
            "query": "Items to carry for Everest expediation","enable-telemetry":True   # Pass the query to the endpoint and enable telemetry to APP Insights
        }
    )

    response = requests.post(f"{url}/chat/products", headers=headers, data=payload)   # Call the endpoint to get LLM response
    print(f"GenAI Response:\n", response)
</code>

2. **Send a GET request for /chat/evaluations**

<code>
    import requests, json
    from urllib.parse import urlsplit

    url_parts = urlsplit(endpoint.scoring_uri)
    url = url_parts.scheme + "://" + url_parts.netloc

    token = ml_client.online_endpoints.get_keys(name=online_endpoint_name).primary_key
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}

    response = requests.get(f"{url}/chat/evaluations", headers=headers)   # Genearete evaluation for the prior LLM conversation
    print(f"Evaluation Response:\n", response)
</code>

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

