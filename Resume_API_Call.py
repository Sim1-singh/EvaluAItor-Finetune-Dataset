import os

import openai
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = 'API_KEY'
filename = 'datasets/resume_hriday_train/10.json'

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
    The conversation consists of questions asked by the interviewer and candidate's answer to them.
    Your task is to summarize the answers of the candidate by topic.
    In order to do so, follow the below steps:- 
    Step 1: First categorize questions asked into project related and experience related and skills related and neither of 3. Disregard the ones under neither of 3.
    Step 2: Then decide what is the topic of the question from project related, experience related and skills related e.g. Hash Table, Computer Networks, Garbage collection in Java, Machine Learning etc.
    Step 3. Summarize the candidate's answers for all the questions on this topic.
    The candidate's complete answer can be in multiple subsequent messages. 
    If the candidate answer is in multiple subsequent messages, consider them as full answer.
    Step 4: Repeat above list of steps for the full conversation
    Few examples delimited by ```:-
    ```
    assistant: Good to know that, Sahil. Moving on to the next question. Could you tell me more about your project Web Scrapper?
    candidate: It allows to scrape information from any page
    interviewer: Could you tell me more about it?
    candidate: .
    interviewer: Please stay focused on the interview.
    candidate: []
    interviewer: As I didn't find any suitable response from you, moving on to the next question. Could you tell me the tech stack that you used for this project?
    candidate: I used python.
    interviewer: Could you elaborate more?
    candidate: I also used requests library in python, apart from that I used Vue JS and Firebase
    interviewer: Interesting, Sahil. Why did you choose a No SQL like Firebase over SQL databases?
    candidate: It was because of faster looktimes and more scalability.
    interviewer: Nice, Sahil. Moving on to the next question. Could you tell me more about your project Chrome Extension?
    candidate: It's a highly customisable chrome extension that allows people to add their favourite webpages to a webpage that displays it all.
    interviewer: Nice, Sahil. Moving on to the next question. Could you tell me the tech stack?
    candidate: Let's skip to the next question
    interviewer: Okay, Sahil. This question is being skipped. Could you tell me your motivation for working on this project?
    candidate: I personally feel that the homepage of Chrome and browsers in general becomes cluttered when you have many favourite pages. To make it look less cluttered and more easier to find, I created this extension. My main motivation to solve this problem for myself.
    interviewer: Impressive, Sahil. Could you tell me more about your experience at Google Cloud?
    candidate: I worked on various Big Data and Machine Learning Projects.
    interviewer: Could you elaborate more?
    candidate: There were several different projects which needed to be completed on the track to complete it. It were from various genre like Big Data and Machine Learning. Projects were taught to make use of cloud computing and deploy on google cloud.
    interviewer: Great, Sahil. Could you tell me more about your learning in Google cloud?
    candidate: Could you review my answer to previous question?
    interviewer: You will be able to see the results once this interview ends.
    candidate: Let's skip to the next question.
    interviewer: Okay, Sahil. This question is being skipped. I can see that you've mentioned Java as your skill. Could you tell me more about it?
    candidate: Let's skip to the next question.
    interviewer: Okay, Sahil. This question is being skipped. Why does Java not make use of pointers?
    candidate: Pointers are quite complicated and unsafe to use by beginner programmers. Java focuses on code simplicity, and the usage of pointers can make it challenging. Pointer utilization can also cause potential errors. Moreover, security is also compromised if pointers are used because the users can directly access memory with the help of pointers.
    interviewer: Correct, Sahil. Explain the use of final keyword in variable, method and class.
    candidate: You are an idiot
    interviewer: Please stay focused on the interview.
    candidate: I don't like you one bit.
    interviewer: As I didn't find any suitable response from you, moving on to the next question.How do you read characters in Java?
    candidate: By using charAt().
    interviewer: Correct, Sahil.Moving on to the next quesion. I can see that you've mentioned Python as your skill. Could you tell me more about it?
    candidate: Let's skip to the next question.
    interviewer: Okay, Sahil.This question is being skipped. What is the use of self in Python?
    candidate: Self is used to represent the instance of the class.
    interviewer: Could you elaborate more?
    candidate: Self is used to represent the instance of the class. With this keyword, you can access the attributes and methods of the class in python. It binds the attributes with the given arguments. self is used in different places and often thought to be a keyword. But unlike in C++, self is not a keyword in Python.
    interviewer: Excellent, Sahil. Could you tell me what an interpreted language is?
    candidate: An Interpreted language executes its statements line by line. For example, Python is an interpreted language.
    interviewer: Correct, Sahil.Thank you for your time. You can click on exit to leave this interview. We will get back to you soon.
    response:- """ + """
        {
        "questions": [
            {
                "topic": "Web Scrapper project",
                "questions_summary": "Could you tell me more about your project Web Scrapper? \\n Why did you choose a No SQL like Firebase over SQL databases?",
                "total_questions_asked": 2,
                "candidate_answer_summary": "The candidate explained that they used python, requests library, vue js and firebase. They used No SQL like firebase over SQL database because of faster looktimes and more scalability."
            },
            {
                "topic": "Chrome Extension project",
                "questions_summary": "Could you tell me more about your project Chrome Extension? \\n Could you tell me the tech stack? \\n Could you tell me your motivation for working on this project?",
                "total_questions_asked": 3,
                "candidate_answer_summary": "The candidate explained that it is a highly customisable chrome extension that allows people to add their favourite webpages to a webpage that displays it all. The candidate skipped the question on tech stack. The candidate explained that they created a browser extension to declutter the homepage of Chrome and other browsers, making it easier to find favorite pages. Their main motivation was to solve this problem for themselves."
            },
            {
                "topic": "Experience at Google Cloud",
                "questions_summary": "Could you tell me more about your experience at Google Cloud? \\n Could you tell me more about your learning in Google cloud?",
                "total_questions_asked": 2,
                "candidate_answer_summary": "The candidate worked on various Big Data and Machine Learning Projects where there were several different projects that needed to be completed on a track and involved the use of cloud computing and deployment on google cloud.The candidate skipped the question asking about their learning at Google Cloud."
            },
            {
                "topic": "Skill - Java",
                "questions_summary": "I can see that you've mentioned Java as your skill. Could you tell me more about it? \\n Why does Java not make use of pointers? \\n Explain the use of final keyword in variable, method and class. \\n How do you read characters in Java?",
                "total_questions_asked": 3,
                "candidate_answer_summary": "The candidate skipped the question asking them to tell more about it. The candidate explained that pointers are quite complicated and unsafe to use by beginner programmers and Java focuses on code simplicity, which means usage of pointers can make it challenging, cause potential errors, and compromises in security when pointers are used because the users can directly access memory with the help of pointers. The candidate did not answer the question on the use of final keyword in variable, method and class. The candidate explained that by using charAt() characters can be read in Java."
            },
            {
                "topic": "Skill - Python",
                "questions_summary": "I can see that you've mentioned Python as your skill. Could you tell me more about it? \\n What is the use of self in Python? \\n Could you tell me what an interpreted language is?"
                "total_questions_asked": 3,
                "candidate_answer_summary": "The candidate skipped the question asking them to tell more about it. The candidate explained that Self is used to represent the instance of the class. With this keyword, the attributes and methods of the class in python can be accessed and it binds the attributes with the given arguments. Self is used in different places and is not a keyword. The candidate explained that python is an interepreted language and an Interpreted language executes its statements line by line."
            }
        ]
    }
    ```
    Summarize the conversation listed below, delimited by triple backticks and give the response in below JSON format:-
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
    Conversation: ```
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
    The interview covers technical topics like projects, work experience and skills like Hash Table, Computer Networks, Garbage collection in Java, Machine Learning etc.
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
                "topic": "Web Scrapper project",
                "questions_summary": "Could you tell me more about your project Web Scrapper? \\n Why did you choose a No SQL like Firebase over SQL databases?",
                "total_questions_asked": 2,
                "candidate_answer_summary": "The candidate explained that they used python, requests library, vue js and firebase. They used No SQL like firebase over SQL database because of faster looktimes and more scalability."
            },
            {
                "topic": "Chrome Extension project",
                "questions_summary": "Could you tell me more about your project Chrome Extension? \\n Could you tell me the tech stack? \\n Could you tell me your motivation for working on this project?",
                "total_questions_asked": 3,
                "candidate_answer_summary": "The candidate explained that it is a highly customisable chrome extension that allows people to add their favourite webpages to a webpage that displays it all. The candidate skipped the question on tech stack. The candidate explained that they created a browser extension to declutter the homepage of Chrome and other browsers, making it easier to find favorite pages. Their main motivation was to solve this problem for themselves."
            },
            {
                "topic": "Experience at Google Cloud",
                "questions_summary": "Could you tell me more about your experience at Google Cloud? \\n Could you tell me more about your learning in Google cloud?",
                "total_questions_asked": 2,
                "candidate_answer_summary": "The candidate worked on various Big Data and Machine Learning Projects where there were several different projects that needed to be completed on a track and involved the use of cloud computing and deployment on google cloud.The candidate skipped the question asking about their learning at Google Cloud."
            },
            {
                "topic": "Skill - Java",
                "questions_summary": "I can see that you've mentioned Java as your skill. Could you tell me more about it? \\n Why does Java not make use of pointers? \\n How do you read characters in Java?",
                "total_questions_asked": 3,
                "candidate_answer_summary": "The candidate skipped the question asking them to tell more about it. The candidate explained that pointers are quite complicated and unsafe to use by beginner programmers and Java focuses on code simplicity, which means usage of pointers can make it challenging, cause potential errors, and compromises in security when pointers are used because the users can directly access memory with the help of pointers. The candidate explained that by using charAt() characters can be read in Java."
            },
            {
                "topic": "Skill - Python",
                "questions_summary": "I can see that you've mentioned Python as your skill. Could you tell me more about it? \\n What is the use of self in Python? \\n Could you tell me what an interpreted language is?"
                "total_questions_asked": 3,
                "candidate_answer_summary": "The candidate skipped the question asking them to tell more about it. The candidate explained that Self is used to represent the instance of the class. With this keyword, the attributes and methods of the class in python can be accessed and it binds the attributes with the given arguments. Self is used in different places and is not a keyword. The candidate explained that python is an interepreted language and an Interpreted language executes its statements line by line."
            }
        ]
    }
    response:-
    {
        "overall_rating": "2.6",
        "overall_summary": "You performed well in some questions but there's room for a lot of improvement.",
        "question_rating": [
            {
                "topic": "Web Scrapper project",
                "question": "Could you tell me more about your project Web Scrapper? \\n Why did you choose a No SQL like Firebase over SQL databases?",
                "candidate_answer_summary": ""
                "rating": 0,
                "total_questions_asked": 2,
                "suggested_answer": "I developed a web scraper app using Python, Requests library, Vue.js, and Firebase.Python was used for backend, Requests library was used for HTTP requests, Vue.js for frontend and Firebase for backend storage",
                "reasoning": "Candidate did not answer any question."
            },
            {
                "topic": "Chrome Extension project",
                "question": "Could you tell me more about your project Chrome Extension? \\n Could you tell me the tech stack? \\n Could you tell me your motivation for working on this project?",
                "candidate_answer_summary": "The candidate explained that it is a highly customisable chrome extension that allows people to add their favourite webpages to a webpage that displays it all. The candidate skipped the question on tech stack. The candidate explained that they created a browser extension to declutter the homepage of Chrome and other browsers, making it easier to find favorite pages. Their main motivation was to solve this problem for themselves."
                "rating": 3,
                "total_questions_asked": 3,
                "suggested_answer": "I used HTML, CSS, and JavaScript for the frontend development of the extension.For backend functionality and data storage, I utilized Firebase, a NoSQL database, due to its fast lookup times and scalability. I also used Chrome's extension API to integrate the extension seamlessly into the browser's interface and functionality.",
                "reasoning": "Candidate did not answer question on tech stack."
            },
            {
                "topic": "Experience at Google Cloud",
                "question": "Could you tell me more about your experience at Google Cloud? \\n Could you tell me more about your learning in Google cloud?",
                "candidate_answer_summary": "The candidate worked on various Big Data and Machine Learning Projects where there were several different projects that needed to be completed on a track and involved the use of cloud computing and deployment on google cloud.The candidate skipped the question asking about their learning at Google Cloud."
                "rating": 3,
                "total_questions_asked": 2,
                "suggested_answer": "The projects were diverse, covering areas like Cloud Computing, Big Data, and Machine Learning, providing a holistic learning experience.I gained hands-on experience in deploying applications on Google Cloud Platform (GCP), managing cloud resources, and utilizing cloud services like Compute Engine, BigQuery, and AI Platform.I learned about the core concepts of cloud computing, including scalability, reliability, and cost-effectiveness.Hands-on labs and tutorials helped me understand how to leverage GCP services effectively for various use cases, from simple web hosting to complex data processing and analysis.",
                "reasoning": "Candidate did not answer the question about their learning at Google Cloud."
            },
            {
                "topic": "Skill - Java",
                "question": "I can see that you've mentioned Java as your skill. Could you tell me more about it? \\n Why does Java not make use of pointers? \\n How do you read characters in Java?",
                "candidate_answer_summary": "I have used java for DSA and some projects. The candidate explained that pointers are quite complicated and unsafe to use by beginner programmers and Java focuses on code simplicity, which means usage of pointers can make it challenging, cause potential errors, and compromises in security when pointers are used because the users can directly access memory with the help of pointers. The candidate explained that by using charAt() characters can be read in Java."
                "rating": 4,
                "total_questions_asked": 3,
                "suggested_answer": "I have been using Java for long time for solving DSA questions and on many projects that I have not mentioned like udent Information System, udent Information System and E-commerce Platform.Java avoids direct pointer manipulation for platform independence, security, automatic memory management, simplicity, and alignment with object-oriented principles. This approach enhances ease of use, reduces memory-related errors, and improves overall program reliability. CharAt() is used for reading characters in Java.",
                "reasoning": "Candidate did not answer the question asking about their experience with Java very well."
            },
            {
                "topic": "Skill - Python",
                "question": "What is the use of self in Python? \\n Could you tell me what an interpreted language is?"
                "candidate_answer_summary": "The candidate explained that Self is used to represent the instance of the class. With this keyword, the attributes and methods of the class in python can be accessed and it binds the attributes with the given arguments. Self is used in different places and is not a keyword. The candidate explained that python is an interepreted language and an Interpreted language executes its statements line by line."
                "rating": 5,
                "total_questions_asked": 2,
                "suggested_answer": "In Python, self is a reference to the instance of the class. It is used within class methods to access variables and methods belonging to that instance.An interpreted language is a type of programming language where the code is executed line by line by an interpreter at runtime, rather than being compiled into machine code beforehand. Python is an example of an interpreted language, which allows for dynamic and interactive coding experiences.",
                "reasoning": "Candidate answered the questions perfectly"
            }
        ]
    }
    Evaluate the conversation below delimited by triple backticks and give the response in below JSON format:-
    """ + """"
    {
        "overall_rating": "<rating>",
        "overall_summary": "<summary>",
        "question_rating": [
            {
                "topic": <topic here>,
                "question": <question here>,
                "candidate_answer_summary": <summarize candidate answer here, empty if no answer>,
                "rating": <rating>,
                "total_questions_asked": <count of total questions asked>,
                "suggested_answer": <your_own_answer_to_the_question>,
                "reasoning": <reasoning>
            }
        ]
    }
    Conversation:- ```
    """

    messages = [
        {
            "role": "user",
            "content": evaluator_system_message + response + "```"
        }
    ]
    # print(messages)
    # response = get_completion_from_messages(messages)
    # print(response)