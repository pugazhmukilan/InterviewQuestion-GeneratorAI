from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
from src.prompt import *
import re

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def fileprocessing(filepath):
    # Load the document from the file
    loader = PyPDFLoader(filepath)
    data = loader.load()

    question_gen = ""
    for page in data:
        question_gen += page.page_content

    splitter_ques_gen = TokenTextSplitter(
    model_name="gpt-3.5-turbo",
    chunk_size = 1000,
    chunk_overlap = 200)

    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)
    document_question_gen = [Document(page_content=t) for t in chunks_ques_gen]
    splitter_ans_gen = TokenTextSplitter(
        model_name = 'gpt-3.5-turbo',
        chunk_size = 1000,
        chunk_overlap = 200)
    
    document_answer_gen = splitter_ans_gen.split_documents(document_question_gen)

    return document_question_gen, document_answer_gen



def llm_pipeline(filepath):
    document_question_gen,document_answer_gen = fileprocessing(filepath)

    llm_ques_gen_pipeline = GoogleGenerativeAI(model="gemini-2.0-flash-001",api_key=GOOGLE_API_KEY)
    
    PROMPT_QUESTIONS = PromptTemplate(input_variables = ["text"],template = prompt_template)
    REFINE_PROMPT_QUESTIONS = PromptTemplate(input_variables=["existing_answer","text"],template= refine_template)

    ques_gen_chain = load_summarize_chain(llm = llm_ques_gen_pipeline,
                                          chain_type = "refine",
                                          question_prompt = PROMPT_QUESTIONS,
                                          refine_prompt = REFINE_PROMPT_QUESTIONS)
    print("question of 5 numbers")
    ques = ques_gen_chain.invoke(document_question_gen[:1])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

    vector_store = FAISS.from_documents(document_answer_gen,embedding=embeddings)
    llm_ans_gen_pipeline = GoogleGenerativeAI(model="gemini-2.0-flash-001",api_key=GOOGLE_API_KEY)
    ANSWER_PROMPT_ANS = PromptTemplate(input_variables=["questions"],template=ANSWER_PROMPT)
    answer_gen_chain = RetrievalQA.from_chain_type(llm = llm_ans_gen_pipeline,
                                            chain_type = "stuff",
                                            retriever = vector_store.as_retriever(),
                                            )
    
   
    ques_list = re.split(r"\n{1,2}", ques['output_text'])
    print(ques_list)
    # ans_list = [answer_gen_chain.run(question) for question in ques_list]
   

    return answer_gen_chain,ques_list

