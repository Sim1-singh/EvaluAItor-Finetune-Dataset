import os

import openai
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = 'API_KEY'
filename = 'datasets/hr_train/HR-Test-Case-59.json'

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
    Step 1: First decide what is the topic of the question e.g. Relocation, Best Project, About Candidate, Strengths & Weaknesses.
    Step 2. Summarize the candidate's answers for all the questions on this topic.The candidate's complete answer can be in multiple subsequent messages.If the candidate answer is in subsequent messages until next topic starts, consider them as full answer.
    Step 3: Repeat above list of steps for the full conversation
    Few examples delimited by ```:-
    ```
    interviewer: Tell me about yourself.
    candidate: My name is Darshan. I am studying bachelors of engineering in Electronics and Instrumentation.
    interviewer: Can you elaborate more on this?
    candidate: I have interest in web development and full stack.
    interviewer: Good to know that Darshan,shall we move on to the next question?
    candidate: yes.
    interviewer: Why should we hire you?
    candidate: I am good at maths which is important for ML, I have diverse knowledge on different frameworks and programming languages like Sweat, React, Angular and Javascript, Java, C.
    interviewer: Good to know that Darshan,shall we move on to the next question?
    candidate: yep.
    interviewer: Could you tell me more about your best project?
    candidate: I would like to quit this round, I am not feeling well.
    interviewer: You can continue this round if you want. Do you want to continue?
    candidate: yes.
    interviewer: Could you tell me more about your best project?
    candidate: I would like to skip this question.
    interviewer: Moving on to the next question,If you won $10 million lotteries, would you still work?
    candidate: I don't like you.
    interviewer: This may carry a negative impression in the evaluation.
    candidate: My best project was a social media app that was used by many people from my college
    interviewer: This may carry a negative impression in the evaluation.
    candidate: No, I won't. I would probably retire.
    interviewer: Nice,shall we continue to the next question?
    candidate: yes
    interviewer: Could you throw some light on your strengths and weaknesses?
    candidate: My strength is my leadership and managerial skills.
    interviewer: And weakness?
    candidate: My weakness would be my slow speed of getting task done as I like it to be done to perfection.
    interviewer: Okay Darshan ,great to talk with you. Thanks for interviewing with us.We will get back to you soon.
    response:- """ + """
        {
        "questions": [
            {
                "topic": "Tell me about yourself.",
                "candidate_answer_summary": "My name is Darshan. I am studying bachelors of engineering in Electronics and Instrumentation.I have interest in web development and full stack."
            },
            {
                "topic": "Why should we hire you?",
                "candidate_answer_summary": "I am good at maths which is important for ML, I have diverse knowledge on different frameworks and programming languages like Svelt, React, Angular and Javascript, Java, C."
            },
            {
                "topic": "Could you tell me more about your best project?",
                "candidate_answer_summary": ""
            },
            {
                "topic": "If you won $10 million lotteries, would you still work?",
                "candidate_answer_summary": "No, I won't. I would probably retire."
            },
            {
                "topic": "Could you throw some light on your strengths and weaknesses?",
                "candidate_answer_summary": "My strength is my leadership and managerial skills.My weakness would be my slow speed of getting task done as I like it to be done to perfection."
            },
        ]
    }
    ```
    Summarize the conversation listed below, delimited by triple backticks and give the response in below JSON format:-
    """ + """"
    {
        "questions": [
            {
                "topic": <topic_name>,
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
    The interview covers technical topics like Relocation, Best Project, About Candidate, Strengths & Weaknesses etc.
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
                "topic": "Tell me about yourself.",
                "candidate_answer_summary": "My name is Darshan. I am studying bachelors of engineering in Electronics and Instrumentation.I have interest in web development,full stack and Machine Learning."
            },
            {
                "topic": "Why should we hire you?",
                "candidate_answer_summary": "I am good at maths which is important for ML having taken many courses in college, I have diverse knowledge on different frameworks and programming languages like Svelt, React, Angular and Javascript, Java, C."
            },
            {
                "topic": "Could you tell me more about your best project?",
                "candidate_answer_summary": ""
            },
            {
                "topic": "If you won $10 million lotteries, would you still work?",
                "candidate_answer_summary": "No, I won't. I would probably retire."
            },
            {
                "topic": "Could you throw some light on your strengths and weaknesses?",
                "candidate_answer_summary": "My strength is my leadership and managerial skills.My weakness would be my slow speed of getting task done as I like it to be done to perfection."
            },
        ]
    }
    response:-
    {
        "overall_rating": "1",
        "overall_summary": "The candidate was able to explain advanatages of python but lacked in understanding of web frameworks. They need to work on it",
        "question_rating": [
            {
                "topic": Tell me about yourself.,
                "candidate_answer_summary": "My name is Darshan. I am studying bachelors of engineering in Electronics and Instrumentation.I have interest in web development,full stack and Machine Learning.",
                "rating": 3,
                "suggested_answer": "My name is Darshan. I am studying bachelors of engineering in Electronics and Instrumentation.I have interest in web development,full stack and Machine Learning. My experience ranges from creation of many web development projects utilizing many of the latest technologies to Deep Learning projects which use implemenations of some of the popular papers for achieving high accuracy.",
                "reasoning": "Candidate's answer lacked depth.'"
            },
            {
                "topic": Why should we hire you?,
                "candidate_answer_summary": "I am good at maths which is important for ML having taken many courses in college, I have diverse knowledge on different frameworks and programming languages like Svelt, React, Angular and Javascript, Java, C.",
                "rating": 5,
                "suggested_answer": "I am good at maths which is important for ML having taken many courses in college, I have diverse knowledge on different frameworks and programming languages like Svelt, React, Angular and Javascript, Java, C.",
                "reasoning": "Candidate's answer is correct.'"
            },
            {
                "topic": If you won $10 million lotteries, would you still work?,
                "candidate_answer_summary": "No, I won't. I would probably retire.",
                "rating": 0,
                "suggested_answer": "Yes, I would still work as I am inspired by this company's motivation and my interest in learning and growing alongside my colleagues.",
                "reasoning": "Candidate's answer is incorrect."
            },
            {
                "topic": Could you tell me more about your best project?,
                "candidate_answer_summary": "",
                "rating": 0,
                "suggested_answer": "My best project involved usage of Tensorflow, Keras and concepts of Transfer Learning to implement Mobile Net Convolution Neural Networks which achieved a high accuracy.I used Keras, Tensorflow to create a base model of Mobile Net and changed its dense layer from 1000 nodes to 1 node and changed activation function from Softmax to Sigmoid. It can be improved by opening more layers for Transfer Learning as I froze most of the layers",
                "reasoning": "The candidate could not answer this question"
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
                "candidate_answer_summary": <summarize candidate answer here>,
                "rating": <rating>,
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
    print(messages)
    response = get_completion_from_messages(messages)
    print(response)