from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

from rag.vector_store import VectorStoreService
from utils.prompt_handler import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model

class RagSummarizeService():
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriver()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self.__init__chain()


    def __init__chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    def retriever_docs(self,query:str)->list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize_docs(self,query:str)->str:

            docs = self.retriever_docs(query)

            context = ""
            counter = 0
            for doc in docs:
                counter += 1
                context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | metadata: {doc.metadata}\n"

            return self.chain.invoke({
                "input": query,
                "context": context
            })


if __name__ == '__main__':
    rag = RagSummarizeService()
    print(rag.rag_summarize_docs("小户型适合哪些扫地机器人"))
