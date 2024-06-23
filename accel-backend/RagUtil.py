import boto3
import os
from dotenv import load_dotenv

load_dotenv()
bedrock_agent_runtime = boto3.client(
    'bedrock-agent-runtime',
    region_name='us-east-1',
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key= os.getenv("AWS_SECRET_KEY")
)


def retrieve(queryInput, kbId, numberOfResults):
    return bedrock_agent_runtime.retrieve(
        knowledgeBaseId = kbId,
        retrievalQuery = {
            'text': queryInput
        },
        retrievalConfiguration = {
            'vectorSearchConfiguration': {
                'numberOfResults': numberOfResults
            }
        },
    )

def retrieveAndGenerate(query, kbId):
    print("calling ret and gen with query: ", query)
    return bedrock_agent_runtime.retrieve_and_generate(
        input={
            'text': query
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kbId,
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-instant-v1'
                }
            }
        )



def get_context(query, kbId, numberOfResults):
    #TODO: toggle this on when sending to our custom model
    #response = retrieve(query, kbId, numberOfResults)
    #return response['retrievalResults']


    response = retrieveAndGenerate(query, kbId)["output"]["text"]
    return response


print(get_context("how much is a flux 300", "AYP1IY3IUL", 10))