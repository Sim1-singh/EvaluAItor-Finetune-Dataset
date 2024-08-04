import os

import openai
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = 'API_KEY'

def get_completion_from_messages(messages,
                                 model="gpt-4-turbo-preview",
                                 temperature=0, max_tokens=1000):
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
    system_message = """

    Step 1: Identify Key Concepts/Topics

    1. Extract a list of 10 topics and concepts pertinent to the job role and display them.
    2. Now use the numbers I provided and select the topics.

    The format of some example responses are given below, strictly follow the exact JSON format :-

    "examples": [
        {
        "job_role": "Java Developer",
        "numbers": {
            "1",
            "3",
            "5",
            "7",
            "9",
            "10"
        },
        "topics": {
            "Object-Oriented Programming (OOP)",
            "Java Collections Framework",
            "Java Generics",
            "Java Database Connectivity (JDBC)",
            "Spring Framework",
            "Java EE (Enterprise Edition)",
            "Concurrency and Multithreading",
            "Java Performance Optimization",
            "JavaFX",
            "Java Persistence API (JPA)"
        }
        "selected_topics": {
            "Object-Oriented Programming (OOP)",
            "Java Generics",
            "Spring Framework",
            "Concurrency and Multithreading",
            "JavaFX",
            "Java Persistence API (JPA)"
        },
        "reason" : "Object-Oriented Programming (OOP) was 1st, Java Generics was 3rd, Spring Framework was 5th, Concurrency and Multithreading was 7th, JavaFX was 9th, Java Persistence API (JPA) was 10th."
        },
        {
        "job_role": "Data Scientist",
        "numbers": {
            "1",
            "3",
            "4",
            "7",
            "10"
        },
        "topics": {
            "Machine Learning Algorithms",
            "Data Preprocessing",
            "Exploratory Data Analysis (EDA)",
            "Model Evaluation and Validation",
            "Natural Language Processing (NLP)",
            "Deep Learning",
            "Big Data Technologies",
            "Data Visualization",
            "Statistical Analysis",
            "Time Series Analysis"
        }
        "selected_topics": {
            "Machine Learning Algorithms",
            "Exploratory Data Analysis (EDA)",
            "Model Evaluation and Validation",
            "Big Data Technologies",
            "Time Series Analysis"
        },
        "reason" : "Machine Learning Algorithms was 1st, Exploratory Data Analysis (EDA) was 3rd, Model Evaluation and Validation was 4th, Big Data Technologies was 7th, Time Series Analysis was 10th."
        }
        ]
        "Numbers" - 
    """

    s = input() #For role input 
    numbers = list(input().split()) #For numbers input (This has to be randomly generated, for testing it is through user input)
    system_message += '[' + ' '.join(numbers) + ']'
    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": s
        }
    ]
    print(messages)
    response = get_completion_from_messages(messages)
    print(response)

    system_message3 = """

    Step1: Use each topic provided in the selected_topic problem once and use it to generate questions in a sequential manner, each increasing in complexity.
    Step2: Ensure the questions are clear, concise, and unambiguous to accurately evaluate the candidate's proficiency.
    Step3: Verify that the questions cover a broad spectrum of skills and knowledge required for the job role and give your reason for choosing it.

    You have to learn from these 2 examples and give the output for the problem in the end, strictly follow the exact JSON format :-

    Example1:
        {
        "job_role": "Java Developer",
        "numbers": {
            "1",
            "3",
            "5",
            "7",
            "9",
            "10"
        },
        "topics": {
            "Object-Oriented Programming (OOP)",
            "Java Collections Framework",
            "Java Generics",
            "Java Database Connectivity (JDBC)",
            "Spring Framework",
            "Java EE (Enterprise Edition)",
            "Concurrency and Multithreading",
            "Java Performance Optimization",
            "JavaFX",
            "Java Persistence API (JPA)"
        }
        "selected_topics": {
            "Object-Oriented Programming (OOP)",
            "Java Generics",
            "Spring Framework",
            "Concurrency and Multithreading",
            "JavaFX",
            "Java Persistence API (JPA)"
        },
        "reason" : "Object-Oriented Programming (OOP) was 1st, Java Generics was 3rd, Spring Framework was 5th, Concurrency and Multithreading was 7th, JavaFX was 9th, Java Persistence API (JPA) was 10th."
        },
    Output1:
        {
        "job_role": "Java Developer",
        "questions": {
            "Q1": "How is polymorphism implemented in Java?",
            "Q2": "What are Java Generics, and how do they enhance type safety and code reusability in Java programming?",
            "Q3": "What is autowiring in spring? What are the autowiring modes?",
            "Q4": "How does Java handle concurrency and multithreading?",
            "Q5": "What is the primary purpose of the Scene class in JavaFX, and how does it relate to the Stage class?",
            "Q6": "What is the role of the EntityManager in JPA, and how does it facilitate interaction with the database?"
        }
        }
    Example2:
        {
        "job_role": "Data Scientist",
        "numbers": {
            "1",
            "3",
            "4",
            "7",
            "10"
        },
        "topics": {
            "Machine Learning Algorithms",
            "Data Preprocessing",
            "Exploratory Data Analysis (EDA)",
            "Model Evaluation and Validation",
            "Natural Language Processing (NLP)",
            "Deep Learning",
            "Big Data Technologies",
            "Data Visualization",
            "Statistical Analysis",
            "Time Series Analysis"
        }
        "selected_topics": {
            "Machine Learning Algorithms",
            "Exploratory Data Analysis (EDA)",
            "Model Evaluation and Validation",
            "Big Data Technologies",
            "Time Series Analysis"
        },
        "reason" : "Machine Learning Algorithms was 1st, Exploratory Data Analysis (EDA) was 3rd, Model Evaluation and Validation was 4th, Big Data Technologies was 7th, Time Series Analysis was 10th."
        }
    Output2:
        {
        "job_role": "Data Scientist",
        "questions": {
            "Q1": "What is Decision Tree?",
            "Q2": "Can you explain the steps you would take to perform EDA on a new dataset?",
            "Q3": "What is F1 Score?",
            "Q4": "What is Hadoop, and how does it facilitate the processing and analysis of large-scale data sets in a distributed computing environment?",
            "Q5": "What are some common methods for handling seasonality in time series data, and can you provide an example of how you would apply one of these methods to a dataset?"
        }
        }
    Now, using these examples solve this problem -

    """

    system_message3 += response

    messages3 = [
        {
            "role": "system",
            "content": system_message3
        }
    ]
    print(messages3)
    response = get_completion_from_messages(messages3)
    print(response)