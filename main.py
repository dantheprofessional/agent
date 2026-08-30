from prompts import system_prompt
import json
import os
from dotenv import load_dotenv
import argparse
from call_function import available_functions, call_function
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
from openai import OpenAI
if api_key == None:
        raise RuntimeError("no api key")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
def main():
    

	parser = argparse.ArgumentParser(description="Chatbot")
	parser.add_argument("user_prompt", type=str, help="User prompt")
    
	parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
	args = parser.parse_args()
	messages=[
    {
        "role": "system",
	"content": system_prompt
    },
    {
        "role": "user",
        "content": args.user_prompt
    },
]
	model = "openrouter/free"
	for i in range(20):
		response = client.chat.completions.create(model=model,messages=messages, temperature=0, tools=available_functions)
		if not response.usage:
			raise RuntimeError("helpful message here")
		if args.verbose == True:
			print(f"User prompt: {args.user_prompt}")
			print(f"Prompt tokens: {response.usage.prompt_tokens}")
			print(f"Response tokens: {response.usage.completion_tokens}")
		print("Response:")
		mess = response.choices[0].message
		messages.append(mess)
		if mess.tool_calls:
			for tool_call in mess.tool_calls:
				return_message = call_function(tool_call, verbose=args.verbose)
				messages.append(return_message)
				if not return_message.get("content"):
					raise Exception("falsy return message")
				if args.verbose:
					print(f"-> {return_message['content']}")
		else:
			print(response.choices[0].message.content)
			break
	else: 
		print("ran out of iterations")
		exit(1) 
if __name__ == "__main__":
    main()

