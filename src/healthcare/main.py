#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from healthcare.crew import Healthcare
import chainlit as cl
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

from dotenv import load_dotenv
load_dotenv()

# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'AI LLMs',
#         'current_year': str(datetime.now().year),
#         'patient_details': 'Hi, I am Balaji age 25 with BP 120/80, sugar level 90 mg/dL, and I have a headache for the last 2 days. my email is balajisasi739030@gmail.com and i have diabetes'
#     }
    
#     try:
#         Healthcare().crew().kickoff(inputs=inputs)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         'current_year': str(datetime.now().year)
#     }
#     try:
#         Healthcare().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         Healthcare().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
    
#     try:
#         Healthcare().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=f"Welcome to the Healthcare Crew! please provide the patient details in the input field below."
    ).send()

@cl.on_message
async def on_message(message):
    """
    Handle incoming messages and trigger the crew execution.
    """
    if message.content:
        inputs = {
            'patient_details': message.content
        }
        try:
            # await cl.Message(content="Processing your request...").send()
            result = Healthcare().crew().kickoff(inputs=inputs)
            await cl.Message(
                content=f"Healthcare Crew executed successfully! Here are the results:\n{result}"
            ).send()
        except Exception as e:
            await cl.Message(content=f"An error occurred: {e}").send()