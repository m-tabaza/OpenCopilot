import os

from extractors.extract_json import extract_json_payload
from models.repository.chat_history_repo import get_all_chat_history_by_session_id
from utils.get_chat_model import get_chat_model
from shared.utils.opencopilot_utils import get_llm
from typing import Optional
from langchain.schema import HumanMessage, SystemMessage
from utils.get_logger import CustomLogger

logger= CustomLogger(module_name=__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = get_llm()


async def gen_params_from_schema(
    param_schema: str, text: str, previous_api_responses: str, current_state: Optional[str]
):
    chat = get_chat_model()

    messages = [
        SystemMessage(
            content="You are an intelligent machine learning model that can produce REST APIs params / query params in json format, given the json schema, user input, data from previous api calls, and current application state."
        ),
        HumanMessage(content="Json Schema: {}.".format(param_schema)),
        HumanMessage(content="prev api responses: {}.".format(previous_api_responses)),
        HumanMessage(content="User's requirement: {}.".format(text)),
        HumanMessage(
            content="Based on the information provided, construct a valid parameter object to be used with python requests library. In cases where user input doesn't contain information for a query, DO NOT add that specific query parameter to the output. If a user doesn't provide a required parameter, use sensible defaults for required params, and leave optional params."
        ),
        HumanMessage(content="Your output must be a valid json, without any commentary"),
    ]
    result = chat(messages)
    logger.info("Generated request body Response: {}".format(result.content))
    d = extract_json_payload(result.content)
    return d
