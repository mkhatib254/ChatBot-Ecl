# Importing essential librairies
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit as cl
from pprint import pprint
import functools
from langchain_community.llms import LlamaCpp
import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
import pytorch_lightning as pl
from datasets import load_dataset


# Path to stored indexes
DB_FAISS_PATH = 'vectorstore/db_faiss'


# The template that limits the Llama 2 interaction in the procedure
custom_prompt_template = """Answer with french only. Rephrase what's provided to you in order to create a meaningful answer, don't try to make up anything

Context: {context}
Question: {question}

Réponds uniquement avec des réponses utiles
Réponse utile:
"""

prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])




# Initialisation du LLM
llm  = LlamaCpp(
    model_path="llama-2-7b-chat.Q4_K_M.gguf",
    temperature=0.75, #Temperature is a quantification to how much the LLM will interfere in the retrieval procedure
   
    top_p=1,   # Quantification to the words that the Llm choose from ( = 1 is the highest)
    
    verbose=True,  # Verbose is required to pass to the callback manager

    n_batch = 120,

    n_gpu_layers =33,
    f16_kv = True   # This settings is only necessary while running on mac gpu
    
)



# Initialisation des embeddings utilisés pour les documents
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'mps'})
db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)







# La partie qui retire de l'information
qa_result = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}), # k is the number of chunks returned after similarity search
                                       return_source_documents=False, # True : gives the document and the page of the answer
                                       chain_type_kwargs={'prompt': prompt}
                                       )


def answer(query):
    response = qa_result({'query': query})
    return response


# Cette partie est pour essayer le chatbot sans interface graphique, vous pouvez l'utiliser

# question = input("Entrez votre question, écrivez exit pour quitter " )
# while question !='exit' :

    

#     print( "Réponse : " , answer(question))
#     question = input("Entrez votre question, écrivez exit pour quitter " )






#chainlit code
@cl.on_chat_start
async def start():
    chain = qa_result
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Bonjour, je suis le bot de la scolarité, comment je peux vous aider?"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain") 
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["result"]
   