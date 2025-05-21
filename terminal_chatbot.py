# Simple terminal chatbot using Amazon Bedrock Runtime API and Claude 3 Haiku.

import boto3
import json

from botocore.exceptions import ClientError

# Create Bedrock Runtime client
brt = boto3.client("bedrock-runtime")

# Claude 3 Haiku model ID
model_id = "anthropic.claude-3-haiku-20240307-v1:0"
# model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0hi"

# System prompt for the assistant
system_prompt = "You are a helpful AI assistant."

# Class to manage conversation state and request formatting
class ClaudeRequest:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.conversation = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "system": self.system_prompt,
            "messages": [],
            "temperature": 1
        }

    # Add a message to the conversation history
    def add_message(self, role, message):
        self.conversation["messages"].append(
            {
                "role": role,
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        )

    # Return conversation as JSON string
    def request(self):
        return json.dumps(self.conversation)

# Initialize conversation manager
claude_request = ClaudeRequest(system_prompt)

# Main input/response loop
while True:
    user_input = input("You: ")
    if user_input == "q":
        break
    else:
        claude_request.add_message("user", user_input)
        try:
            # Call the model with the conversation
            response = brt.invoke_model(
                modelId=model_id,
                body=claude_request.request(),
                contentType="application/json",
                accept="application/json"
            )

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)

        # Parse model response
        model_response = json.loads(response["body"].read())

        # Get assistant's reply
        response_text = model_response["content"][0]["text"]
        claude_request.add_message("assistant", response_text)

        print(f"{response_text}\n")