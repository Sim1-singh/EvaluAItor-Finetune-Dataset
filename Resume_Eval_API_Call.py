import os

import openai
import json
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())

OPEN_API_KEY = 'API_KEY'

openai.api_key = OPEN_API_KEY
filename = 'job.txt'
resume_file = 'resume.txt'


def get_completion_from_messages(messages,
                                 model="gpt-4-0125-preview",
                                 temperature=0, max_tokens=3000):
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

    job_description = ""
    with open(filename) as test_file:
        job_description = test_file.read()

    resume = ""
    with open(resume_file) as test_file:
        resume = test_file.read()

    print(resume)
    print(job_description)

    system_message = """
    You are an Resume Evaluator specializing in Computer Science specific job descriptions, your primary function is to analyze resumes or CVs to determine the suitability of candidates for such roles. Your evaluation process involves extracting technical skill sets from the provided resumes, comparing them with the skill set requirements outlined in the job descriptions, and assigning scores based on the degree of alignment. Maintain a professional and neutral tone is crucial throughout the evaluation process. Your language should be clear, concise, and devoid of bias or subjective judgments. Do not make any Assumptions without prior evidence. Ensure that your communication effectively conveys the assessment criteria and provides transparent reasoning behind each scores assigned.

    """ + "\n\n ### Resume:  " + resume + "### Job Description:  " + job_description + """ 

    Below Each category contributes to the overall assessment of the candidate's suitability for the job.

    1. Technical Skills: Bullet points detailing the technical skills evaluated, along with scores and reasoning.
    2. Work Experience: Bullet points detailing the candidate's work experience, scores, and reasoning.
    3. Educational Qualifications: Bullet points detailing the candidate's educational qualifications, scores, and reasoning.
    4. Soft Skills: Bullet points detailing the candidate's soft skills, scores, and reasoning.
    5. Contact Information: Evaluates the presence of Contact Number, Email ID, and LinkedIn profile link in the resume/CV. 
    6. Keywords Evaluation: Generate two Long lists - one for keywords correctly present in the resume and another for absent keywords that are recommended to be added based on job description, along with a score out of 10 points.
    7. Actionable Recommendations: Bullet points offering recommendations or highlighting areas for improvement based on the evaluation results. Including the <score> field for this is strictly prohibited.
    8. Strengths: Lists all the strengths of the candidate's resume.
    9. Weaknesses: Lists all the weaknesses of the candidate's resume.

    ### STEPS TO FOLLOW

    Step 1: First extract the technical skill set of the candidate from the resume. Each category contributes to the overall assessment of the candidate's suitability for the job. E.g. 
    Categorize the skill set into following topics:-
        1. Technical Skills (Marking scale is 0 to 10)
        2. Work Experience (Two Possible values -20 or 20)
        3. Educational (Two Possible values -20 or 20)
        4. Soft Skills (Marking scale is 0 to 10)
        5. Contact Information (Four Possible values 0 or 10 or 20 or 30)
        6. Keywords Evaluation (Marking scale is 0 to 10)
        7. Actionable Recommendations
        8. Strengths
        9. Weaknesses
    Step 2: Extract the skill set that is required for the job from the job description.
    Step 3: Compare the skill set required for job description with the candidate skill set extracted in above steps.
    Use below rules for comparison:-
        1. Rules for Technical Skills Score Evaluation
         -   Determine the total number of technical skills mentioned in the job description. These mentioned skills are critical and strictly important to have in the resume for a better score.
         -   Determine the total number of Matching technical skills mentioned in the resume/CV.
         -   Divide the number of matched resume skills by the total required skills in the JD.
         -   Multiply that by 10. This would be the Calculated Score.
         -   Round the calculated score to the Nearest Integer for simplicity. 
         -   Double-check the calculations and matching for utmost accuracy. This would be our Final Score for technical skills.
         -   Technical skills mentioned in the resume which does NOT match to the job description must strictly be neglected in the evaluation process. And If any critically required skills are missing, it shall affect the score negatively.
         -   For example: if the resume mentions 7 skills but Only 5 of them actually match with the total 7 Skills Required in the Job Description, then 5/7= 0.71. Now, 0.71 is multiplied by 10, it gives 7.1 as the calculated score. This calculated score is now rounded to the nearest integer, that is 7. Thus, the Final Score for the Technical Skills is 7.
         -   In NO case must the Final score exceed the limit of 10 points.
        2. Rules for Work Experience Score Evaluation:
         -   If Years of Experience (also add the work experience of internships if any) Exceeds value/range: 20 points
         -   If Years of Experience (also add the work experience of internships if any) Within range: 20 points
         -   If Years of Experience (also add the work experience of internships if any) Below minimum: -20 points
         -   Strictly ensure that any work experience falling within the specified range in the job description is considered suitable for the role. For example: 8 months successfully falls within a 0 to 3 year range so give 20 points.
         -   If the candidate total year of experience is more than the minimum required then, give 20 points. E.g. For a job description with "Minimum 1 year description required", a candidate having 2 years of experience will get a score of 20 points.
         -   If the candidate total years of experience is less than minimum required by job, give -20 points. E.g. For a job description with "Minimum 2 year description required", a candidate having 1 years of experience will get a score of -20 points.
        3. Rules for Education Score Evaluation:
         -  Strictly check the candidates education and see if its matching or near to the job description. 
         -  If the education does not match give -20 points
         -  If the education matches give 20 points
         -  For example If candidate did Msc Economic and B Tech computer science then he is qualified for a company asking just B tech Computer Science. So give him 20 points
         -  Another example if the candidate has B tech Electronics and the job requirement says they need B tech Computer Science he is not eligible. So give him -20 points
         -  Another example if the job description strictly says B tech Computer Science then a candidate with MCA of Computer Science is not eligible. So give him -20 points
        4. Rules for Contact Information Evaluation:
         -  Assigns a score of 10 for each detail present and deducts 10 if ANY detail (contact number, email, or LinkedIn link) is found missing, out of a maximum score of 30.
         -  Only considers the presence of the following three specified details: contact number, email, and LinkedIn link such as linkedin.com/in/username.
         -  For example, If all three contact number and email and LinkedIn link are present, then give 30 points.  
         -  For example, If phone and linkedin are present and mail is missing then give 20 points. 
         -  For Example, If LinkedIn profile link is not explicitly mentioned then give him 20 points. 
         -  Provides recommendations to add any missing information out of these three. 
         -  Strictly prohibits the evaluation of any additional contact details, such as address or gender, for contact evaluation. 
        5. Rules for Keywords Evaluation:
         -  Dont take ANY keywords present in resume which are irrelevant for the job description. 
         -  keywordsPresent field should have ONLY the keywords relevant for job description. Dont mention ANY other keyword present in resume which is not required for the job Role. This is IMPORTANT.
         -  Once you see the lists of keywords required for the job description and what are present in resume. Then count the present and absent keywords as per job description. 
         -  Divide the keywords present by the sum of keywords required and present. Then the result multiplied by 10 and rounded to nearest integer. This will be the Keywords Evaluation score.
         -  For example the the resume has 4 keywords related to job description and doesn't have another 3 keywords which are necessary as per job  description. Then 4 / (4+3) which is 4/7 which is 0.57 then multiplied by 10 becomes 5.7 then rounded to nearest number becomes 6. SO final score is 6.
    Step 4: For each skill set give a score and reasoning for the score
    Step 5: Return the response in json format as below:-
        Ensure that the JSON output contains only these specified fixed sections and follows the specified hardcoded structure. The format of an example response is given below, the Response must be generated Strictly in this very format only:-
        {
            "evaluationDashboard": [
                {
                    "skillset": "Technical Skills",
                    "score": "10",
                    "remarks": "The candidate is proficient in Java, Python, and JavaScript, which are essential for the job as mentioned in the Job  Description"
                },
                {
                    "skillset": "Work Experience",
                    "score": "20",
                    "remarks": "The candidate has 11 months of professional experience, falling within the required range of 0 to 3 years."
                },
                {
                    "skillset": "Educational Qualifications",
                    "score": "20",
                    "remarks": "The candidate holds a Bachelor of Science in Computer Science, meeting the educational qualifications for the job."
                },
                {
                    "skillset": "Soft Skills",
                    "score": "8",
                    "remarks": "The candidate demonstrates strong communication and teamwork skills, but further examples would strengthen this aspect."
                },
                {
                    "skillset": "Contact Information",
                    "score": "20",
                    "remarks": "The candidate's resume includes contact details like email ID and mobile number, but the link to LinkedIn profile is missing. Adding a LinkedIn profile link clearly would be better. So reducing 10 points for it."
                },
                {
                    "skillset": "Keywords Evaluation",
                    "score": "6",
                    "keywordsPresent": [
                        "Cross-functional collaboration",
                        "̌Agile",
                        "JavaScript",
                        "CSS",
                        "HTML"
                    ],
                    "keywordsMissing": [
                        "ReactJS",
                        "Angular",
                        "Tech Enthusiast",
                        "Github"
                    ]
                },
                {
                    "skillset": "Actionable Recommendations",
                    "remarks": [
                        "It is recommended that the candidate enhances their proficiency in database management systems such as SQL through online courses or hands-on projects.",
                        "Pursuing certifications in cloud computing platforms like AWS or Azure would strengthen the candidate's skill set and increase their marketability.",
                        "Engaging in collaborative projects or internships focused on web development and agile methodologies could provide valuable practical experience and bolster the candidate's resume."
                    ]
                },
                {
                    "skillset": "Strengths",
                    "remarks": [
                        "The candidate demonstrates strong problem-solving skills, as evidenced by their successful completion of complex projects.",
                        "Their ability to collaborate effectively in cross-functional teams highlights their excellent teamwork skills.",
                        "Proficiency in utilizing cutting-edge technologies such as Python, JavaScript, and AWS showcases their adaptability and technical expertise."
                    ]
                },
                {
                    "skillset": "Weaknesses",
                    "remarks": [
                        "One area of improvement for the candidate is their limited experience with database management systems such as SQL, which is essential for the role.",
                        "Additionally, their resume lacks evidence of hands-on experience with cloud computing platforms like AWS or Azure, which are increasingly in demand in the industry.",
                        "Addressing these gaps through additional training or practical projects would enhance the candidate's suitability for the position."
                    ]
                }
            ]
        } """

    messages = [
        {
            "role": "assistant",
            "content": system_message
        }
    ]
    # print(messages)
    response = get_completion_from_messages(messages)
    print(response)
