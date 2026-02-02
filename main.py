import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI API KEY not found. Make sure it is in the .env file.")

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="AIagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # user_prompt = input("User: ")
    user_prompt = args.user_prompt

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)]
        )
    ]
    
    # messages = [
    #     types.Content(
    #         role="user", 
    #         parts=[types.Part(text=args.user_prompt)]
    #     )
    # ]

    #prompt = args.user_prompt

#     response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=messages,
#     config=types.GenerateContentConfig(
#         system_instruction=system_prompt,
#         temperature=0,
#         tools=[available_functions],
#     ),
# )

    # try:
    #     response = client.models.generate_content(
    #         model="gemini-2.5-flash",
    #         contents=messages,
    #         config=types.GenerateContentConfig(
    #             tools=[available_functions],
    #             system_instruction=system_prompt,
    #         ),
    #     )
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return

    MAX_ITERATIONS = 20

    for _ in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"Error: {e}")
            return

        # 1️⃣ Add model candidates to conversation history
        if not response.candidates:
            raise RuntimeError("Model returned no candidates")

        for candidate in response.candidates:
            messages.append(candidate.content)

        # 2️⃣ If no function calls → FINAL ANSWER
        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        # 3️⃣ Handle function calls
        function_responses = []

        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts")

            fr = function_call_result.parts[0].function_response
            if fr is None or fr.response is None:
                raise RuntimeError("Invalid function response")

            # Print result (tests rely on this)
            print(fr.response["result"])

            function_responses.append(function_call_result.parts[0])

        # 4️⃣ Feed tool results back to the model
        messages.append(
            types.Content(
                role="user",
                parts=function_responses,
            )
        )

    # 5️⃣ Safety net
    print("Error: agent did not finish within iteration limit")
    exit(1)



#     response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=messages,
#     config=types.GenerateContentConfig(
#         system_instruction=system_prompt,
#         tools=[available_functions],
#     ),
# )
    #function_calls = response.function_calls

    # if function_calls:
    #     for function_call in function_calls:
    #         print(
    #             f"Calling function: {function_call.name}({function_call.args})"
    #         )
    # else:
    #     print(response.text)
    
    function_results = []

    if response.function_calls:
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=args.verbose)

            # Sanity checks (required by assignment)
            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts")

            fr = function_call_result.parts[0].function_response
            if fr is None:
                raise RuntimeError("Function response missing")

            if fr.response is None:
                raise RuntimeError("Function response payload missing")

            # Collect result for later (important for next assignments)
            function_results.append(function_call_result.parts[0])

            print(fr.response["result"])
            if args.verbose:
                print(f"-> {fr.response}")

    else:
        print(response.text)
    


if __name__ == "__main__":
    main()
