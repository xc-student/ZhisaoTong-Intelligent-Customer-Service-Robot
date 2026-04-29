from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community. chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from utils.config_handle import rag_config,agent_config


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional [Embeddings | BaseChatModel]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional [Embeddings | BaseChatModel]:
        return ChatOpenAI(model=rag_config["chat_model_name"],api_key=agent_config["Qwen_API_KEY"],base_url=agent_config["Qwen_BASE_URL"])

class EmbeddingModelFactory(BaseModelFactory):
    def generator(self) -> Optional [Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"],dashscope_api_key=agent_config["DASHSCOPE_API_KEY"])


chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()
