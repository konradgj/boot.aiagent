import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    args = sys.argv[1:]
    
    if not args:
        print('No prompt provided. Exiting')
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(model=model, contents=messages)   

    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
