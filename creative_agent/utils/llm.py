from functools import lru_cache
from os import getenv

from langchain_openai import AzureChatOpenAI, ChatOpenAI


@lru_cache(maxsize=4)
def get_model():

    return AzureChatOpenAI(
        model="gpt-4o",
        api_version="2024-08-01-preview",
    )
