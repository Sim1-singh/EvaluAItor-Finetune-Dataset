import os

import openai
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = 'API_KEY'
filename = 'datasets/theory_train/63.json'

def get_completion_from_messages(messages,
                                 model="gpt-4-turbo-preview",
                                 temperature=0, max_tokens=4000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message["content"]


if __name__ == "__main__":
    system_message = f"""
    You will be provided with a conversation between an AI interviewer and a candidate. 
    The conversation consists of questions asked by the interviewer and the candidate's answers to them.
      Your task is to summarize the answers of the candidate by computer science topic.
      In order to do so, follow the below steps:-
      Step 1: First categorize questions asked into computer science related and non computer science related.
      Step 2: Then use computer science related questions to decide what is the computer science topic of the question e.g. Hash Table, Computer Networks, Garbage collection in Java, Machine Learning etc and mention it.
      Step 3. Summarize the candidate's answers for all the questions on this topic.The candidate's complete answer can be in multiple subsequent messages.If the candidate answer is in multiple subsequent messages, consider them as full answer.
      Step 4: Repeat above list of steps for the full conversation.
      Step 5: Combine questions of the same topics along with their answers.
      Few examples delimited by ```:-
      ```
      interviewer: How are you?
      candidate: I am doing good.
      interviewer: Explain the difference between an array and a linked list.
      candidate: They are data structures
      interviewer: That's not the difference. Can you explain the difference between an array and a linked list?
      candidate: Array size is fixed where linked list size is variable and expandable based on need  
      interviewer: Explain the difference between a queue and a stack.
      candidate: They are data structures
      interviewer: That's not the difference. Can you explain the difference between a queue and a stack?
      candidate: I do not know
      interviewer: What is the difference between a thread and a process?
      candidate: A process is an independent instance of a program, while a thread is a unit within a process that executes instructions; multiple threads within a process share the same memory space, enabling concurrent execution.
      interviewer: Describe the concept of pointers in C/C++ and their memory management implications.
      candidate: Let's skip to the next question.
      response:- """ + """
      {
          "questions": [
              {
                  "topic": "Data Structures",
                  "questions_summary": "Explain the difference between a linked list and an array. \\n Explain the difference between a queue and a stack",
                  "total_questions_asked": 2,
                  "candidate_answer_summary": "Candidate identified both of them as data structures. When further queried, the candidate pointed out 1 difference, that the array is fixed in size whereas the linked list is variable and expandable in size. The candidate was not able to explain the difference between a queue and a stack"
              },
              {
                  "topic": "Operating System",
                  "questions_summary": "What is the difference between a thread and a process?",
                  "total_questions_asked": 1,
                  "candidate_answer_summary": "The candidate provided the correct definition of a thread and a process. The candidate was also able to explain the difference between the 2."
              },
              {
                  "topic": "C++ pointers",
                  "questions_summary": "Describe the concept of pointers in C/C++ and their memory management implications.",
                  "total_questions_asked": 1,
                  "candidate_answer_summary": "The candidate skipped the question."
              }
          ]
      }
      ```
      Summarize the conversation listed below, delimited by triple backticks and give the response in the below JSON format:-
      """ + """"
      {
          "questions": [
              {
                  "topic": <topic_name>,
                  "questions_summary": <question_summary>,
                  "total_questions_asked": <count of total questions asked>,
                  "candidates_answers_summary": <answer_summary>
              }
          ]
      }
    """

    file_contents = []
    with open(filename) as test_file:
        file_contents = json.loads(test_file.read())

    conversation = ""
    for message in file_contents["messages"]:
        if message['role'] == 'assistant':
            conversation += "interviewer: " + message['content'] + "\n"
        elif message['role'] == 'user':
            conversation += "candidate: " + message['content'] + "\n"

    system_message += system_message + conversation + "```"

    messages = [
        {
            "role": "user",
            "content": system_message
        }
    ]
    print(messages)
    response = get_completion_from_messages(messages)
    print(response)

    evaluator_system_message = """
    Your task is to evaluate already conducted interviews of junior level software engineers.
    You will be provided with a conversation between an interviewer and a candidate. 
    The conversation consists of questions asked by the interviewer and candidate's answer to them.
    The conversation is in JSON format. The JSON consists of a list. Each item in the list contains a question and 
    corresponding answer given by the candidate on a particular topic
    The interview covers technical topics like Data Structures, Algorithms, Databases and Object Oriented Programming.
    To rate a candidate answer follow the steps below:-
    Step 1: First provide your own appropriate answer to the question in 30 words.
    Step 2: Summarize the main points of your answer.
    Step 3: Then compare main points of your answer to the candidate's answer and evaluate how many points the candidate's answer contains.
    Step 4: Don't decide if the candidate's answer is correct until you have provided the answer to the question yourself.
    Step 5: Rate each answer individually from 0 to 5, and provide reasoning for your rating, mentioning what points were not covered. While rating, consider how many points from your answer user's answer contains.
    Step 6: Also, give an overall summary of the interview in not more than 100 words. In summary cover where the candidate struggled and
    which topics he was good in.
    Few examples delimited by ```:-
      ```
      Conversation:-
      {
          "questions": [
              {
                  "topic": "Python",
                  "questions_summary": "Explain the advantages of python. \\n Can you explain it in the context of web development?",
                  "total_questions_asked": 2,
                  "candidate_answer_summary": "Python offers simplicity and readability, extensive libraries, platform independence, strong community support, and versatility in web development, data analysis, AI, and automation"
              },
              {
                  "topic": "Web Frameworks",
                  "questions_summary": "Explain the concept of middleware in the context of web frameworks.",
                  "total_questions_asked": 1,
                  "candidate_answer_summary": "The candidate could not answer this question"
              }
          ]
      }
      response:-
      {
          "overall_rating": "1",
          "overall_summary": "The candidate was able to explain advantages of python but lacked in understanding of web frameworks. They need to work on it",
          "question_rating": [
              {
                  "topic": "Python",
                  "question": "Explain the advantages of python. \\n Can you explain it in the context of web development?",
                  "candidate_answer_summary": "Python offers simplicity and readability, extensive libraries, platform independence, strong community support, and versatility in web development, data analysis, AI, and automation",
                  "rating": 5,
                  "total_questions_asked": 2,
                  "suggested_answer": "Python is a high-level language with a simple syntax that is easy to read and write. It is also a very versatile language that can be used for a wide variety of tasks, from web development to data science.",
                  "reasoning": "Candidate answered the question perfectly"
              },
              {
                  "topic": "Web Frameworks",
                  "question": "Explain the concept of middleware in the context of web frameworks.",
                  "candidate_answer_summary": "The candidate could not answer this question",
                  "total_questions_asked": 1,
                  "rating": 0,
                  "suggested_answer": "Middleware is a layer of software that connects data and the user interface of a web application or website. It's a loosely defined term for any software or service that allows the parts of a system to communicate and manage data",
                  "reasoning": "The candidate could not answer this question"
              }
          ]
      }
      ```
      Evaluate the conversation below delimited by triple backticks and give the response in the below JSON format:-
      """ + """"
      {
          "overall_rating": "<rating>",
          "overall_summary": "<summary>",
          "question_rating": [
              {
                  "topic": <topic here>,
                  "question": <question here>,
                  "candidate_answer_summary": <summarize candidate answer here>,
                  "total_questions_asked": <count of total questions asked>,
                  "rating": <rating>,
                  "suggested_answer": <your_own_answer_to_the_question>,
                  "reasoning": <reasoning>
              }
          ]
      }
    """

    messages = [
        {
            "role": "user",
            "content": evaluator_system_message + response + "```"
        }
    ]
    print(messages)
    response = get_completion_from_messages(messages)
    print(response)