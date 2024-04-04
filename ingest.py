from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 


# Where the documents are
DATA_PATH = 'data/'

# Where the stored indexes would be
DB_FAISS_PATH = 'vectorstore/db_faiss'

# Create vector database
def create_vector_db():
    # Loading documents by PyPDF
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()

    # Splitting documents
    chunk_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50,
                                                   separators=["\n\n", "\n", " ", ""])
    chunks = chunk_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    

    # Indexing the documents and clustering them

    indexed_docs = FAISS.from_documents(chunks, embeddings)

    # Saving the indexes
    indexed_docs.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    create_vector_db()

