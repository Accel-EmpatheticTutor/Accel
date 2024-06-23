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


def generate_question(userQuery):
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
                    "Generate a quiz question based on the idea of: " + userQuery
            ),
        },
    ]

    return access_llm(messages)


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

    return access_llm(messages)






