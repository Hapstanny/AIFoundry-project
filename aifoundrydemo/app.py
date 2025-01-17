import sys, os, json
from flask import Flask, request
from pathlib import Path
import pandas as pd
from config import enable_telemetry,get_logger,ASSET_PATH
from chat_with_products import chat_with_products,create_chat_eval_data
from evaluate import evaluate_results
import multiprocessing
import contextlib

logger = get_logger(__name__)
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "ok"


@app.route("/health", methods=["GET"])
def health():
    return "healthy"


@app.route("/chat/products", methods=["POST"])
def chat_products():
    body = request.get_json()
    for key, value in body.items():
        logger.info(f"🤖 {key}: {value}")
        if key == "query":
            query = body["query"]
        elif key == "enable-telemetry" and value is True:
            enable_telemetry(True)

    try:
        response = chat_with_products(messages=[{"role": "user", "content": query}])
        logger.info(f"Return Response: {response}")
        
        evaldata=[{"query": query, "response": response}]
    
        home_directory=os.environ.get('HOME')
        logger.info("Home Directory:" + home_directory)

        create_chat_eval_data(json.dumps((evaldata[0])), home_directory + "/chat_eval_data.jsonl")

        return response
    except Exception as e:
        logger.error(f"🤖 Error: {e}")
    
@app.route("/chat/evaluations", methods=["GET"])
def get_chat_evaluations():
    try:

        enable_telemetry(True)

        home_directory=os.environ.get('HOME')
        logger.info("Home Directory:" + home_directory)

        # check if path is accessible
        if os.path.exists(home_directory + "/chat_eval_data.jsonl"):
            logger.info("File Exists")
            eval_results=evaluate_results(home_directory , "chat_eval_data.jsonl")
        
            tabular_result = pd.DataFrame(eval_results.get("rows"))

            logger.info("-----Summarized Metrics-----")
            logger.info(eval_results["metrics"])
            logger.info("-----Tabular Result-----")
            logger.info(tabular_result)
            logger.info(f"View evaluation results in AI Studio: {eval_results['studio_url']}")

            os.remove(home_directory + "/chat_eval_data.jsonl")
            return eval_results
        else:
            logger.info(home_directory + "/chat_eval_data.jsonl" + " does not exist")
            raise Exception("Previous evaluate_results doesn't exists, Run the chat_products API to generate chat_eval_data.jsonl file")
        
        
    except Exception as e:
        logger.error(f"🤖 Error: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)