import hashlib
import os
from os.path import exists
from logger_hander import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TxtLoader, TextLoader


def get_file_md5_hex(file_path:str) :

    if not exists(file_path):
        logger.error(f"[md5 calculation]File {file_path} does not exist")
    if not os.path.isfile(file_path):
        logger.error(f"[md5 calculation]File {file_path} is not file")

    md5_obj = hashlib.md5()

    chunk_size = 4096
    try:
        with open(file_path,"rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[md5 calculation]File {file_path} failded calculation of file md5，{e}")
        return None

def listdir_with_allowed_type(path: str,allowed_types: tuple[str]):
    result_files = []

    if not os.path.isdir(path):
        logger.error(f"[file path]Directory {path} is not directory")
        return allowed_types
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            result_files.append(os.path.join(path,f))
    return tuple(result_files)
def pdf_loader (path:str,password=None)->list[Document] :
    return PyPDFLoader(path,password).load()


def txt_loader (path:str)->list[Document] :
    return TextLoader(path).load()