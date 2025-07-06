import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
import functions.file_helpers as f_helper


def main():
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("No prompt provided. Exiting")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    prompt = " ".join(args)
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    available_functions = types.Tool(
        function_declarations=[
            f_helper.schema_get_files_info,
            # f_helper.schema_get_file_content,
            # f_helper.schema_write_file,
        ]
    )

    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        return response.text
    for fcp in response.function_calls:
        print(f"Calling function: {fcp.name}({fcp.args})")


if __name__ == "__main__":
    main()
