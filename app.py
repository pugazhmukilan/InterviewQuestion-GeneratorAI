# from fastapi import FastAPI,Form,Request,Response,File,Depends,HTTPException,status
# from fastapi.responses import RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from fastapi.encoders import jsonable_encoder

# import uvicorn
# import os
# import aiofiles
# import json
# import csv
from src.helper import llm_pipeline

# app = FastAPI()
# # Mount the 'static' directory to serve static files (CSS, JS, images, etc.) at the '/static' URL path
# app.mount("/static", StaticFiles(directory="static"), name="static")


# templates = Jinja2Templates(directory="templates")

import streamlit as st
import os
import pandas as pd

# Ensure output directory exists
os.makedirs("static/docs",exist_ok = True)
os.makedirs("static/output", exist_ok=True)

st.set_page_config(page_title="PDF Processor", layout="centered")
st.title("📄 PDF Upload & CSV Generator")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

import streamlit as st
import pandas as pd
import os
import time  # For simulating wait if needed
Done = False
if uploaded_file and not Done:
    pdf_path = f"static/docs/{uploaded_file.name}"
    os.makedirs("static/docs", exist_ok=True)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Initialize progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    # Step 1: Extract questions from PDF
    status_text.text("🔍 Running LLM pipeline...")
    progress_bar.progress(10)
    generator, questions = llm_pipeline(pdf_path)
    progress_bar.progress(30)
    print(questions)
    # Step 2: Generate answers
    final_answers = []
    total = len(questions)
    if total == 0:
        st.error("❌ No questions generated.")
    else:
        for idx, question in enumerate(questions):
            status_text.text(f"✍️ Generating answer {idx + 1} of {total}...")
            answer = generator.invoke(question)["result"]
            final_answers.append(answer)
            progress_percent = 30 + int(((idx + 1) / total) * 50)  # from 30% to 80%
            progress_bar.progress(progress_percent)

        # Step 3: Create and save CSV
        status_text.text("📦 Saving to CSV...")
        data = {"Questions": questions, "Answers": final_answers}
        df = pd.DataFrame(data)
        csv_path = "static/output/QuestionAnswer.csv"
        os.makedirs("static/output", exist_ok=True)
        df.to_csv(csv_path, index=False)
        progress_bar.progress(100)
        status_text.text("✅ Done!")

        # Show preview
        st.subheader("📊 Processed CSV Preview")
        st.dataframe(df)
        Done  = True
        # Download button
        with open(csv_path, "rb") as f:
            st.download_button(
                label="⬇️ Download CSV",
                data=f,
                file_name="output.csv",
                mime="text/csv"
            )
        #stop further exectuing something
        

# generator,questions = llm_pipeline(r"C:\Users\PUGAZH\Desktop\Projects\GenAi - Projects\LangChain-Projects\Resource\flutter.pdf")
    



# for question in questions:
#     answer = generator.invoke(question)["result"]
#     print("Question : "+question+"\n")
#     print("Answer :"+answer+"\n")
#     with open("answers.txt","a", encoding="utf-8") as file:
#         file.write(question+"\n")
#         file.write("Answer: "+answer+"\n")
#         file.write("---------------------------------")
#         file.write("\n")
