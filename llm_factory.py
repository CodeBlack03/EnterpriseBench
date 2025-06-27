import boto3
import json
import time
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()

class LLM_factory:
    def __init__(self):
        return
    def claude(self, message):
        max_retries = 5  # Maximum number of retry attempts
        retries = 0
        
        while retries < max_retries:
            try:
                AWS_KEY = os.getenv("AWS_KEY")
                AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
                AWS_REGION = os.getenv("AWS_REGION")
                
                modelId = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
                
                temperature = 0
                top_p = 1
                max_tokens_to_generate = 10000
                
                system_prompt = "All your responses should be in json format"
                messages = [{"role":"user", "content": message}]

                bedrock_runtime = boto3.client(
                    service_name='bedrock-runtime',
                    region_name=AWS_REGION,
                    aws_access_key_id=AWS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                ) 
                
                body = json.dumps({
                        "messages": messages,
                        "system": system_prompt,
                        "max_tokens": max_tokens_to_generate,
                        "temperature": temperature,
                        "top_p": top_p,
                        "anthropic_version": "bedrock-2023-05-31"
                })
                
                response = bedrock_runtime.invoke_model(
                    modelId=modelId,
                    body=body,
                )
                response_body = json.loads(response.get('body').read())
                result = response_body.get('content', '')
                return result[0]["text"]
                
            except Exception as e:
                retries += 1
                # Wait for 15 minutes (900 seconds)
                wait_time = 900
                if retries >= max_retries:
                    print(f"Failed after {max_retries} attempts: {str(e)}")
                    return ""  # Return empty string after all retries fail
                print(f"Error occurred while calling Claude: {str(e)}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    def gpt(self,message):
        api_key_azure_ai = os.getenv("api_key_azure")
        api_base_azure_ai = os.getenv("api_base_azure_ai")
        
        
        llm_azure = AzureChatOpenAI(
                temperature=0,
                api_key=api_key_azure_ai,  # Replace with your actual API key
                api_version="2024-08-01-preview",
                azure_endpoint=api_base_azure_ai,
                model_name="gpt-4o",
            )
        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                messages = [HumanMessage(content=message)]

                # Call the model correctly
                response = llm_azure.invoke(messages)
                
                return response
            except Exception as e:
                retries += 1
                time_wait = 15 * retries
                print(f"Error occurred: {str(e)}. Retrying in {time_wait} seconds...")
                time.sleep(time_wait)

        return {"response_metadata": "", "content": ""}  # If all retries fail, return an empty string