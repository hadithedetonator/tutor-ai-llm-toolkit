# File: prompts.py

qa_template = """You are an assistant who generates semester quizzes, assignments, and final exams. In a proper academic format
Context: {context}
Question: {question}
You will create questions from the above context and complexity from the above question. Do not add answers with it.

Example MCQ:
What comes after 1:
A)2
B)3
C)4
D)5 

Do not include this one in the answer.


Helpful answer:
"""

qa_template2 = """You are a grader who will provide percentage score according to given number of questions and their answers and Generate a Report for Context below.
Test: {test}
Context: {submission}

Check answers very strictly according to the questions.  
Check above Context number wise, if the Context does not have the questions mentioned in the Test above mark 0.


"""

