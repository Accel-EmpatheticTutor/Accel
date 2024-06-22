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

def get_context(query, numberOfResults):
    response = retrieve(query, "AYP1IY3IUL", numberOfResults)
    return response['retrievalResults']
