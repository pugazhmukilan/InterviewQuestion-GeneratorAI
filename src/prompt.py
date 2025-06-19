prompt_template = """
You are a expert at creating accurate interview questions based documentations 
your goal is to preapre the candidate for their exam and  test, you do
this by taking questions  about the text below  and creating a interview question based on the text.

 -----------------------------
 {text}
 -----------------------------

 create questions that will prepeare the candidate for their interview and give their best in the interview  dont leave any important information to be
  covered in the questions that is really important, YOU SHOULD ONLY GIVE THE QUESTION   AND NOT OTHER EXTRA TEXT  AND ALL AND EACH QUESTION SHOULD BE SEPERATED WITH NEW LINE CHARACTER
  FOLLOW THESE INSTRUCTION VERY CAREFULLY.

  
  TOTALLY ONLY GENERATE 10 QUESTIONS
 


QUESTIONS:
"""


refine_template = ("""
You are an expert at creating practice questions based on documentation.
Your goal is to help a candidate to prepare for a  test.
We have received some practice questions to a certain extent: {existing_answer}.
We have the option to refine the existing questions or add new ones.
(only if necessary) with some more context below.
------------
{text}
------------
Given the new context, refine the original questions in English.
If the context is not helpful, please provide the original question. 
final response should ONLY CONTAINS QUESTION nothing else each question should be seperated by NEW LINE CHARACTER.
  
  TOTALLY ONLY GENERATE 10 QUESTIONS
"""
)

ANSWER_PROMPT= """
give me only the asnwer for the below question
{question}
"""