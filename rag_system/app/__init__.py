import boto3
from botocore.config import Config
from langchain_aws import BedrockLLM, BedrockEmbeddings

llm_model_id = 'anthropic.claude-v2:1'
embeddings_model_id = 'amazon.titan-embed-text-v1'

bedrock_client = boto3.client(service_name='bedrock-runtime', region_name="us-east-1",
                              config=Config(read_timeout=3600,
                                            connect_timeout=3600))
textract_client = boto3.client('textract', region_name="us-east-1")

anthropic_llm = BedrockLLM(
                    model_id=llm_model_id,
                    model_kwargs={
                        "max_tokens_to_sample": 4000,
                        "temperature": 0.00,
                        "top_p": 1,
                        "top_k": 0,
                        "stop_sequences": [],
                    },
                    client=bedrock_client,
                )

bedrock_embeddings = BedrockEmbeddings(model_id=embeddings_model_id, client=bedrock_client)