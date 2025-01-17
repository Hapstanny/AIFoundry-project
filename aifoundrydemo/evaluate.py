import os
import pandas as pd
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ConnectionType
from azure.ai.evaluation import evaluate
from azure.ai.evaluation import GroundednessEvaluator,CoherenceEvaluator,RelevanceEvaluator
from azure.identity import DefaultAzureCredential

from chat_with_products import chat_with_products
from config import ASSET_PATH
from pathlib import Path
from opentelemetry import trace
from config import ASSET_PATH,get_logger, enable_telemetry


logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)

from dotenv import load_dotenv

load_dotenv()
home_directory=os.environ.get('HOME')
        

@tracer.start_as_current_span(name="evaluations")
def evaluate_results(evalpath,evalfile) -> dict:

    # create a project client using environment variables loaded from the .env file
    project = AIProjectClient.from_connection_string(
        conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
    )

    connection = project.connections.get(connection_name=os.environ["AOAI_CONNECTION_NAME"], include_credentials=True)

    evaluator_model = {
        "azure_endpoint": connection.endpoint_url,
        "azure_deployment": os.environ["EVALUATION_MODEL"],
        "api_version": "2024-06-01",
        "api_key": connection.key,
    }

    # groundedness = GroundednessEvaluator(evaluator_model)
    coherence = CoherenceEvaluator(evaluator_model)
    relevance= RelevanceEvaluator(evaluator_model)

    import datetime
    now = datetime.datetime.now()

    logger.info(evalpath + "/" + evalfile)

    result = evaluate(
        data=str(evalpath + "/" + evalfile),
        # target=evaluate_chat_with_products,
        evaluation_name="evaluate_chat_with_products_" + now.strftime("%Y-%m-%d_%H-%M-%S"),
        evaluators={
            # "groundedness": groundedness,
            "coherence": coherence,
            "relevance": relevance
        },
        evaluator_config={
            "default": {
                "query": {"${data.query}"},
                "response": {"${data.response}"}
            }
        },
        azure_ai_project=project.scope,
        output_path= evalpath + "/myevalresults.json",
    )

    # print(f"View evaluation results in AI Studio: {result['studio_url']}")

    return result
