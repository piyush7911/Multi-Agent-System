# agents/agent_base.py

import openai
from abc import ABC, abstractmethod
from loguru import logger
import os
from dotenv import load_dotenv

class AgentBase(ABC):
    def __init__(self, name, max_retries=2, verbose=True):
        self.name = name
        self.max_retries = max_retries
        self.verbose = verbose

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def call_openai(self, messages, temperature=0.7, max_tokens=150):
        retries = 0
        while retries < self.max_retries:
            try:
                if self.verbose:
                    logger.info(f"[{self.name}] Sending messages to OpenAI:")
                    for msg in messages:
                        logger.debug(f"  {msg['role']}: {msg['content']}")
                client = openai.OpenAI(
                    api_key="AIzaSyAbBHbu3pQru4LY8sa-J7oPUBmrL7GBvko",
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                )
                response = client.chat.completions.create(
                    model="gemini-1.5-pro",
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                reply = response.choices[0].message.content
                if self.verbose:
                    logger.info(f"[{self.name}] Received response: {reply}")
                return reply
            except Exception as e:
                retries += 1
                logger.error(f"[{self.name}] Error during OpenAI call: {e}. Retry {retries}/{self.max_retries}")
        raise Exception(f"[{self.name}] Failed to get response from OpenAI after {self.max_retries} retries.")
