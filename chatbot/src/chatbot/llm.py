from langchain_community.llms import Ollama
from chatbot.config import config

llm = Ollama(model=config.OPENAI_MODEL_NAME, base_url=config.OPENAI_API_BASE)