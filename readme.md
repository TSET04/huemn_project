# Self-Improving AI Agent

## Overview

This project implements a **self-improving AI agent** capable of performing tasks using external tools while learning from its own mistakes. The primary focus is on **behavior improvement and feedback loops**.  

The agent executes tasks, evaluates its performance, identifies mistakes, and maintains a **failure memory** to reduce repeated errors in future runs.  

---

## Features

- Executes tasks with **tool-assisted workflows**.
- Tracks **tool usage and sequence** to detect mistakes.
- Records past errors in a **failure memory**.
- Adjusts behavior based on recurring mistakes.
- Evaluates each run explicitly with clear reasoning.
- Demonstrates improvement over time in handling tasks correctly.

---

## Agent Design

### Purpose

The agent in this implementation acts as a **research assistant**:

- Receives user queries.
- Performs **web searches** when required.
- Summarizes search results before producing a final answer.

### Available Tools

| Tool Name           | Description                              | Usage Requirement       |
|---------------------|------------------------------------------|-------------------------|
| `search_web`        | Searches the web for relevant information| Required                |
| `summarize_results` | Summarizes results from previous tool    | Required                |

### Mistake Handling

The agent tracks and learns from the following types of mistakes:

- Not using a required tool.
- Using an incorrect tool.
- Calling tools in the wrong sequence.
- Producing a final answer too early.
- Misusing or ignoring tool outputs.

---

## System Components

1. **Mistral AI Client**  
   - Handles conversation with the LLM.
   - Generates responses and decides when to use tools.

2. **Tools Mapping and Execution**  
   - Maps tool names to Python functions.
   - Executes tools when called by the agent.
   
3. **Failure Memory**  
   - Tracks frequency and type of mistakes.
   - Guides agent behavior in subsequent runs.

4. **Evaluation Module**  
   - Checks if the correct sequence of tools was used.
   - Validates that a final answer was produced.
   - Provides clear reasons for failure.

5. **Prompt Builder**  
   - Generates system prompts including past mistakes.
   - Encourages the agent to avoid repeating errors.

---

## How to Run this Code

1. Create a virtual Environment using the command 'python -m venv <virtual_env_name>'.
2. Install the requirements using the command 'pip install -r requirements.txt'.
3. Configure the MistralAI API key in the '.env' folder.
4. Run the 'main.py' file

### NOTES: This Code aims to implement the self-learning capabilities of an LLM. The model learns through its mistakes and makes effective and better decisions in the future. During testing, the main while loop runs endlessly so to escape it, use 'ctrl + c'.