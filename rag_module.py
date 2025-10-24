from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# load docs
docs = CSVLoader("faqs.csv").load()

# build index
emb = OpenAIEmbeddings(model="text-embedding-3-small")
vs = FAISS.from_documents(docs, emb)

def refer_to_docs(user_prompt):
    q = user_prompt
    matches = vs.similarity_search(q, k=3)
    for m in matches:
        print(m.page_content)
    return(matches)

### tests - passed
# response = refer_to_docs("medisave")
# print(type(response))
# print(response[0])


