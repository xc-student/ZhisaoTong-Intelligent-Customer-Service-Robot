from langchain_chroma import Chroma
from utils.config_handle import chrom_config
from utils.logger_hander import logger
from utils.path_tool import get_abs_path
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import txt_loader,pdf_loader,listdir_with_allowed_type,get_file_md5_hex
import os

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chrom_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chrom_config["persist_directory"]),
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chrom_config["chunk_size"],
            chunk_overlap=chrom_config["chunk_overlap"],
            separators=chrom_config["separators"],
            length_function=len
        )

    def get_retriver(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chrom_config["k"]})


    def load_document(self):

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chrom_config["md5_hex_store"])):
                open(get_abs_path(chrom_config["md5_hex_store"]),"w").close()
                return False
            with open(get_abs_path(chrom_config["md5_hex_store"]), "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False

        def save_md5(md5_for_check: str):
            with open(get_abs_path(chrom_config["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_document(path: str):
            if(path.endswith(".txt")):
                return txt_loader(path)
            if(path.endswith(".pdf")):
                return pdf_loader(path)
            return []

        allowed_files = listdir_with_allowed_type(get_abs_path(chrom_config["data_path"]),chrom_config["allowed_type"])

        for file in allowed_files:
            md5_hex = get_file_md5_hex(file)
            if  check_md5_hex(md5_hex):
                logger.info(f"MD5 hex {md5_hex}内容已存在")
                continue
            try:
                document:list[document] = get_file_document(file)
                if not document:
                    logger.warning(f"[加载知识库]{file}内没有有效文本内容,跳过")
                    continue

                split_documents = self.spliter.split_documents(document)
                if not split_documents:
                    logger.warning(f"[加载知识库]{file}分片后没有有效文本内容，跳过")
                    continue
                self.vector_store.add_documents(split_documents)
                save_md5(md5_hex)
                logger.info(f"[加载知识库]{file} 内容加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{file}加载失败:{str(e)}")


if __name__ == '__main__':
    service = VectorStoreService()
    service.load_document()

    retriver = service.get_retriver()
    invoke = retriver.invoke("迷路")
    for document in invoke:
        print(document.page_content)
        print("-"*20)