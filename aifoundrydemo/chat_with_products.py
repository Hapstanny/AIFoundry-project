import os
from pathlib import Path
from opentelemetry import trace
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import ConnectionType
from config import ASSET_PATH, get_logger, enable_telemetry
import json


# initialize logging and tracing objects
logger = get_logger(__name__)
tracer = trace.get_tracer(__name__)


from azure.ai.inference.prompts import PromptTemplate


@tracer.start_as_current_span(name="chat_with_products")
def chat_with_products(messages: list, context: dict = None) -> dict:

    try:
        # create a project client using environment variables loaded from the .env file

        project = AIProjectClient.from_connection_string(
            conn_str=os.environ["AIPROJECT_CONNECTION_STRING"], credential=DefaultAzureCredential()
        )

        # create a chat client we can use for testing
        chat = project.inference.get_chat_completions_client()

        if context is None:
            context = {}

        # do a grounded chat call using the search results
        grounded_chat_prompt = PromptTemplate.from_prompty(Path(ASSET_PATH) / "grounded_chat.prompty")

        system_message = grounded_chat_prompt.create_messages(context=context)
        # print(f"🤖 System message: {system_message}")
        response = chat.complete(
            model=os.environ["CHAT_MODEL"],
            messages=system_message + messages,
            **grounded_chat_prompt.parameters,
        )

        response_content = json.dumps(response.choices[0].message.content)
        return {"message": response_content}
    
    except Exception as e:
        logger.error(f"Error: {e}")


def create_chat_eval_data(data, file_path):
    with open(file_path, "a") as f:
        f.write(data)
        f.write("\n")

