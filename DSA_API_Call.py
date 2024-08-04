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
Your response should look like this separated by 3 backticks:
```
{
  "Title": "Here's the evaluation of the provided code snippet based on some important criteria:",
  "Ratings": {

    "Correctness": {
      "rating": "X.X",
      "feedback": "One-liner feedback about Correctness"
    },
    "CodeStructure andReadability": {
      "rating": "X.X",
      "meaningful_var": "X.X",
      "meaningful_com":"X.X",
      "feedback": "One-liner feedback about Code Structure and Readability"
    },
    "AlgorithmEfficiency": {
      "rating": "X.X",
      "feedback": "One-liner feedback about Algorithm Efficiency"
    },
    "OverallCodeEvaluation": {
      "rating": "X.X",
      "feedback": "One-liner feedback about Overall Code Evaluation"
    },
    "finalFeedback": "Concise 2 liner summary about the overall code quality"
  }

}
```
For your reference, below is the exact example of how your response should look be structured separated by 3 backticks:
```
{
  "Title": "Here's the evaluation of the provided code snippet based on some important criteria:",
  "Ratings": {
    "Correctness": {
      "rating": "3.5",
      "feedback": "The code correctly finds a pair of elements in the input vector 'a' whose sum equals the given target. However, it doesn't handle the case where there is no such pair, and it simply returns an empty vector. It would be better to handle this scenario more explicitly with a meaningful return value or message."
    },
    "CodeStructureAndReadability": {
      "rating": "3.0",
      "meaningful_var": "3",
      "meaningful_com":"0",
      "feedback": "The code lacks comments , making it less readable. It would be beneficial to add comments explaining the purpose of the code blocks. The indentation is consistent, which is good for readability."
    },
    "AlgorithmEfficiency": {
      "rating": "2.5",
      "feedback": "The current code has a time complexity of O(n^2) due to the nested loops, where 'n' is the size of the input vector. This is not efficient for larger inputs, and a more efficient algorithm like using a hash table (unordered_map) to store seen elements and their indices could reduce the time complexity to O(n)."
    },
    "OverallCodeEvaluation": {
      "rating": "2.9",
      "feedback": "The code works for small inputs and provides a correct answer. However, it lacks robustness, efficiency, and readability. It can be improved by handling edge cases, using better variable names, adding comments, and employing a more efficient algorithm."
    },
    "finalFeedback": "Overall, the code needs some improvements to make it more reliable and efficient, especially for larger input sizes."
  }
}
```
Rules enclosed in 3 backticks:
```
1) All scores will be out of five and read the question and tell me what you understand.
2) Think of 5 examples cases where each case is an edge case for the question provided. The cases that work will add 1 point to Correctness score.
3) Create 2 variables - meaningful_var  which has maximum score of 3 and meaningful_com which has maximum score of 2. Search the entire code for variable names and add 1  point for each variable with meaningful name to meaningful_var. Now search the entire code for comments and add 1 point for each comment  to meaningful_com. Now add meaningful_var and meaningful_com to CodeStructureAndReadability.
4) Search the entire code and check if any meaningful improvements can be made to improve its space and time complexity. For every improvement possible, deduct one point in AlgorithmEfficiency.
5) Your answer should be in form of a JSON Object.
```
Question separated by 3 backticks:
    """
s2 = """
Solution separated by 3 backticks:
```
"""  
with open('question_dsa.txt', 'r') as file:
  question = file.read().replace('\n', '')
with open('code_dsa.txt', 'r') as file:
  code = file.read().replace('\n', '')
system_message = system_message + question + "```" + s2 + code + "```"

messages = [
    {
        "role": "user",
        "content": system_message
    }
]
print(messages)
response = get_completion_from_messages(messages)
print(response)