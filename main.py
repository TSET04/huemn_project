import os
import json
from mistralai import Mistral
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

# CONFIG
MODEL = "mistral-large-latest"
TEMPERATURE = 0.8
MAX_TOKENS = 50

# Tools Functions 
def search_web(**kwargs):
    return "Web search executed."

def summarize_results(**kwargs):
    return "Summary created from search results."

# Tools Mapping
TOOLS_MAP = {
    "search_web": search_web,
    "summarize_results": summarize_results
}

# Tools Definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for relevant information",
            "parameters": {"type": "object"}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_results",
            "description": "Summarize the search results",
            "parameters": {"type": "object"}
        }
    }
]

# Memory to store failures
failure_memory = defaultdict(int)

# Prompt Builder which includes failure memory
def build_system_prompt(failure_memory):
    base = (
        "You are a helpful assistant.\n"
        "Always learn from your mistakes. Never repeat any mistake. Be very careful and responsible when making decisions.\n"
    )

    if failure_memory:
        base += "\nPAST ERRORS:\n"
        for error, count in failure_memory.items():
            if error == "total":
                continue
            base += f"- {error} (occurred {count} times)\n"

    return base

# Evaluation Function
def evaluate_run(tool_sequence, final_answer_given):
    expected = ["search_web", "summarize_results"]

    if tool_sequence != expected:
        return False, f"Incorrect tool order. Expected {expected}, got {tool_sequence}"

    if not final_answer_given:
        return False, "Final answer was not produced"

    return True, "Success"

# Mistral Client
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

while True:
    user_query = input("User: ")
    if not user_query:
        break

    messages = [
        {
            "role": "system",
            "content": build_system_prompt(failure_memory)
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    tool_sequence = []
    final_answer_given = False

    while True:
        response = client.chat.complete(
            model=MODEL,
            messages=messages,
            tools=tools,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        assistant_msg = response.choices[0].message
        messages.append(assistant_msg)

        # Final answer
        if assistant_msg.content and not assistant_msg.tool_calls:
            final_answer_given = True
            # print("Assistant:", assistant_msg.content)
            print("The AI Response is hidden for evaluation purposes.")
            break

        # Tool calls handling
        if assistant_msg.tool_calls:
            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name
                tool_sequence.append(tool_name)

                print(f"[Tool Used] -> {tool_name}")

                args = json.loads(tool_call.function.arguments or "{}")
                result = TOOLS_MAP[tool_name](**args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            break
    
    # Evaluating the response
    success, reason = evaluate_run(tool_sequence, final_answer_given)

    if success:
        print("Run Successful")
        print("Tool order:", tool_sequence)
    else:
        print("Run Failed")
        print("Reason:", reason)
        print(f"Tool order:{tool_sequence}")

        # Maintaining failure memory
        failure_memory["total"] += 1
        failure_memory[reason] += 1
    
    print(f"Failure Memory:{dict(failure_memory)}", end="\n\n")
