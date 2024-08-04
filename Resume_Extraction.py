import os

import openai
import json
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

openai.api_key = 'API_KEY'

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
    system_message = """
    Example of JSON format delimited in 3 backticks.
```
EXAMPLE 1:
{
    "Projects":{
        "Project1":{
            "Title":"Implementing Feed Forward Neural Network",
            "Information": "N/A"
        },
        "Project2":{
            "Title":"Classifying Chattering Process through images",
            "Information":"Currently working on a project on classifying chattering processes under a professor under Mechanical Engineering Department.Currently highest achieved accuracy is 98 percent, used data augmentation techniques to achieve a bigger dataset and more unique data and trained it on different CNN architectures."
        }
    },
    "Work Experience":{
        "Work Experience1":{
            "Company":"Evaluaitor",
            "Information":"Worked on creation of a chatbot like experience for DSA and HR round interviews.Implemented strategies to optimize the model’s performance through refined prompts.Created and curated data specifically for fine-tuning purposes.",
            "Reason": "Was the most detailed."
        }
    },
    "Skills":{
        "Skill1":"numpy",
        "Skill2":"pandas",
        "Skill3":"tensorflow",
        "Skill4":"matplotlib",
        "Skill5":"SQL",
        "Skill6":"MongoDB",
        "Skill7":"Angular",
        "Skill8":"Vue",
        "Skill9":"C++",
        "Skill10":"Java"
    }
}
```
```
EXAMPLE 2:
{
    "Projects":{
        "Project1":{
            "Title":"Artificial Intelligence with Python Projects",
            "Information": "N/A"
        },
       "Project2":{
            "Title":"N/A",
            "Information":"N/A"
        }
    },
    "Work Experience":{
        "Work Experience1":{
            "Company":"Young Minds Technology Solutions Pvt Ltd",
            "Information":"Internship Completion Certificate",
            "Reason": "It is the most recent experience and relevant to the field of computer science."
        }
    },
    "Skills":{
        "Skill1":"Python programming",
        "Skill2":"Machine Learning",
        "Skill3":"Embedded Design and IoT",
        "Skill4":"Linux Operating System",
        "Skill5":"Machine Learning",
        "Skill6":"Internet of Things",
        "Skill7":"English",
        "Skill8":"Telugu",
        "Skill9":"Hindi"
    }
}
```
```
EXAMPLE 3:
{
    "Projects":{
        "Project1":{
            "Title":"Weather Forecasting Application",
            "Information": "Designed and developed a weather forecasting application, utilizing modern technologies and APIs to deliver accurate and real-time weather information to users."
        },
        "Project2":{
            "Title":"N/A",
            "Information":"N/A"
        }
    },
    "Work Experience":{
        "Work Experience1":{
            "Company":"N/A",
            "Information":"N/A",
            "Reason": "No experience found."
        }
    },
    "Skills":{
        "Skill1":"numpy",
        "Skill2":"pandas",
        "Skill3":"tensorflow",
        "Skill4":"matplotlib",
        "Skill5":"SQL",
        "Skill6":"MongoDB",
        "Skill7":"Angular",
        "Skill8":"Vue",
        "Skill9":"C++",
        "Skill10":"Java"
    }
}
```
```
EXAMPLE 4:
{
    "Projects":{
        "Project1":{
            "Title":"Automatic Question Generation using NLP",
            "Information": "Built a question generator for producing assessments like MCQs, True/False questions"
        },
        "Project2":{
            "Title":"Automated Trading Bot for Day Trading",
            "Information":"Engineered automated Trading Bots with Python and Amazon Web Services (AWS). Employed Python libraries like Numpy, Pandas, Matplotlib, scikit-learn, Keras and Tensorflow."
        }
    },
    "Work Experience":{
        "Work Experience1":{
            "Company":"N/A",
            "Information":"N/A",
            "Reason": "No experience found."
        }
    },
    "Skills":{
        "Skill1":"Python",
        "Skill2":"Google Dialogflow",
        "Skill3":"NLP",
        "Skill4":"BERT",
        "Skill5":"OpenAI GPT-2",
        "Skill6":"T5 transformers"
    }
}
```
You have to read this data below and give it in form of json file containing only skills, projects and their work experience.
```
    """
resume = """
mit Kumar   Ó   +91-7073653180 Roll No.: 1si20cs010   R   amit.1si20cs010@gmail.com Siddaganga Institute Of Technology, Tumkur, Karnataka      GitHub Profile  ¯   LinkedIn Profile  Education  Class 10 : Loyola School, 2017  Class 12 : Parkmount Public School, Danapur, 2019  Bachelor of Technology in Computer Science : Siddaganga Institute Of Technology, Tumkur, 2020-2024 (CGPA: 7.51)  Personal Projects  Movix Project : A web-based application for movie enthusiasts to login, search for movies, and apply filters to retrieve information from an API.  –   Implemented user authentication for secure login functionality.  –   Integrated with an external API to fetch movie data.  Blockchain Project : Decentralized applications using Ethereum and Solidity  –   Developed smart contracts for various use cases, such as token creation and transfer.  –   Tested and deployed the application on the Ethereum blockchain.  Security System using C++ : Software-based security system  –   Implemented encryption and decryption algorithms to secure data transmission.  –   Integrated with hardware components for biometric authentication.  2048 Game using JavaScript : Front-end development and game logic  –   Implemented game mechanics such as merging tiles and generating new tiles.  –   Designed a responsive user interface with smooth animations.  Movie Project using DBMS : Database management system for storing movie data  –   Designed and implemented database schema for storing movie data.  –   Implemented queries for searching, sorting, and filtering movie information.  Crime Visualization using Machine Learning : Machine learning model to visualize crime data  –   Used machine learning algorithms for analyzing crime data and predicting patterns.  –   Developed a visualization tool to display the analyzed data in an interactive format.  Technical Skills and Interests  Languages : C, C++, HTML, CSS, JavaScript  Libraries : C++ STL, Python Libraries  Web Dev Tools : Node.js, VSCode, Git, GitHub  Framework : React.js  Cloud/Databases : MySQL  Relevant Coursework : DSA, Operating Systems,DBMS,Computer Networks, SQL, OOP  Areas of Interest : Web Development, Cloud Security  Problem Solving : 600 problems on different platforms, LeetCode Rank 1800, Knight  Experience  Team Leader, Decoder : Conducted various hackathons, fostering innovation and collaboration, awarded prizes, and promoted skill development (Sit)
"""
rules = """
Rules enclosed in 3 backticks:

```
1. Search the entire data and before adding it to Work experience see that it should not include hackathons, competitions or education. It should involve startup or a company and work should be related to computer science.
2. If the number of work experience is greater than 1, summarise all work experience individually by yourself and choose only one with maximum information and give your reasoning for choosing it in the reason part of experience.
3. Search the entire data for computer science related projects and non computer science related projects. Disregard the non computer science related projects. Display the first and seventh computer science related projects. 
4. Search through data for skills and classify them as computer science related and non computer science related. Display only computer science related skills and individually without any header.
5. Use examples only for learning the format of JSON file.
```
"""

system_message += system_message + resume + "\n```\n" + rules

messages = [
    {
        "role": "user",
        "content": system_message
    }
]
print(messages)
response = get_completion_from_messages(messages)
print(response)