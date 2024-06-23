import boto3
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def access_llm(query):
    #TODO: change this to our custom llm
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"), base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3-sonar-small-32k-online",
        messages=query,
    )

    return response

def predictQuiz(query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user. Your primary job will be to decide if the user is trying to get you to quiz them. Examples of a user wanting to switch to quiz mode would be \"can you quiz me?\", \"quiz me?\", \"please quiz me\", \"test me\"."
            ),
        },
        {
            "role": "user",
            "content": (
                    "Evaluate if the user wants you to quiz them. Respond with only 1 word, true or false. Here is the user's most recent message: " + query
            ),
        },
    ]

    evaluation = (access_llm(messages))
    res = evaluation.choices[0].message.content
    return res
def generate_question(history):
    stringHistory = ""
    count = 0
    for message in history:
        count += 1
        stringHistory += ("Message" + str(count) + ": " + message['message'] + ".")

    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user. Your primary job will be to generate quiz questions based on a specific topic provided by the user."
            ),
        },
        {
            "role": "user",
            "content": (
                    "Generate a quiz question to quiz the user based on recent conversation messages. Here is the conversation, with the earliest message listed as message 1, and the most recent message as the highest number: " + stringHistory
            ),
        },
    ]

    res =  access_llm(messages)
    return res.choices[0].message.content


def check_answer(originalQuestion, userAnswer):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user. Your primary job will be to review answers to users and check if they are correct."
            ),
        },
        {
            "role": "user",
            "content": (
                    "Evaluate the user's answer to see if it is correct or close to correct. Explain if necessary, but the first word of your response must be true if you determine the answer to be correct and false if you determine the answer to be wrong. The original question was " + originalQuestion + " and the users's reponse was " + userAnswer
            ),
        },
    ]

    res = access_llm(messages)
    return res.choices[0].message.content


# print(predictQuiz("can you quiz me?"))




