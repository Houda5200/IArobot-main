from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.chains.question_answering import load_qa_chain

directory = '/mnt/d/Epitech/Chatbot/fable.txt'
# A modifier

def load_docs(directory):
  loader = TextLoader(directory)
#   print(loader)
  documents = loader.load()
#   print(documents)
  return documents

documents = load_docs(directory)
len(documents)

def split_docs(documents,chunk_size=100,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)
# print(len(docs))

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(docs, embeddings)
query = "What are the different kinds of pets people commonly own?"
matching_docs = db.similarity_search(query)

matching_docs[0]

persist_directory = "chroma_db"
vectordb = Chroma.from_documents(
    documents=docs, embedding=embeddings, persist_directory=persist_directory
)
vectordb.persist()

template = """Question: {question}
Answer: Let's work this out in a step by step way to be sure we have the right answer."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="/mnt/d/Epitech/Chatbot/llama-2-7b-chat.Q8_0.gguf",
    # A modifier (télécharger le LLM : https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q8_0.gguf)
    temperature=0.75,
    max_tokens=100,
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)

chain = load_qa_chain(llm, chain_type="stuff",verbose=True)

print("Bonjour, dites moi tout en quoi puis je vous aider")
query = input()
# query = "What are the emotional benefits of owning a pet?"
matching_docs = db.similarity_search(query)
answer =  chain.run(input_documents=matching_docs, question=query)
answer
print("La réponse : " + str(answer))
