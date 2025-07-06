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
            f_helper.schema_get_file_content,
            f_helper.schema_write_file,
            f_helper.schema_run_python_file,
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
        res = call_function(fcp, verbose)
        if not res.parts[0].function_response.response:
            raise Exception("Error: function response missing")
        if verbose:
            print(f"-> {res.parts[0].function_response.response}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    name = function_call_part.name
    args = {"working_directory": "./calculator"}
    func_dict = {
        "get_files_info": f_helper.get_files_info,
        "get_file_content": f_helper.get_file_content,
        "write_file": f_helper.write_file,
        "run_python_file": f_helper.run_python_file,
    }
    if "directory" in function_call_part.args:
        args["directory"] = function_call_part.args["directory"]
    if "file_path" in function_call_part.args:
        args["file_path"] = function_call_part.args["file_path"]
    if "content" in function_call_part.args:
        args["content"] = function_call_part.args["content"]
    if "args" in function_call_part.args:
        args["args"] = function_call_part.args["args"]
    if name not in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    result = func_dict[name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )


if __name__ == "__main__":
    main()
