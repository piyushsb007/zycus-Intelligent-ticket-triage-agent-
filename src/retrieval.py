# ===================================================================================================
# RAG (Retrieval-Augmented Generation) component
# ---------------------------------------------------------
# 1. Load all Markdown knowledge-base documents. 
# 2. Split documents into overlapping chunks. 
# 3. Embed chunks using a sentence-transformer model.  
# 4. Store embeddings in a local ChromaDB vector database. 
# 5. Retrieve the most similar chunks for an incoming ticket.
# ===================================================================================================
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load all Markdown files from the knowledge base directory and create a vector store for retrieval
loader = DirectoryLoader(
    "knowledge-base",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

documents = loader.load()
if not documents: 
    raise RuntimeError("No Markdown files found under knowledge-base/")

# Split the documents into smaller chunks for better retrieval/RAG performance
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def retrieve_kb(query: str, top_k: int = 3):
    docs = retriever.invoke(query)
    results = []
    for d in docs:
        source = d.metadata.get("source", "unknown")
        results.append({
            "document": source.replace("knowledge-base/", ""),
            "content": d.page_content
        })
    return results[:top_k]