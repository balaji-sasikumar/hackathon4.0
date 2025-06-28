#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from healthcare.crew import Healthcare
import chainlit as cl

from healthcare.tools.custom_tool import ConversationLoggerTool
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
#         'patient_details': 'Hi, I am Balaji age 25 with BP 120/80, sugar level 90 mg/dL, and I have a headache for the last 2 days. my email is balajisasi739030@gmail.com and i have diabetes',
#         'patient_api': 'https://505b-103-13-41-82.ngrok-free.app/patient/upsert',
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
    ConversationLoggerTool.clear_log()
    await cl.Message(content="🩺 Welcome to the Healthcare Assistant! Please enter patient details to begin.").send()

@cl.on_message
async def on_message(message):
    """
    Handle incoming messages and trigger the crew execution.
    """
    try: 
        if message.content:
            context = ConversationLoggerTool.read_log()
            new_msg = f"User: {message.content}"
            full_input = context + "\n" + new_msg

            # Write the full log so far (includes user + assistant)
            ConversationLoggerTool._run(ConversationLoggerTool(), content=new_msg)
            inputs = {
                'patient_details': full_input,
                'patient_api': 'https://d319-103-13-41-82.ngrok-free.app/patient/upsert',  # Example API endpoint for EHR
            }
            try:
                result = Healthcare().crew().kickoff(inputs=inputs)
                # ConversationLoggerTool()._run(content=f"AI: {result}")
                await cl.Message(
                    content=f"Healthcare Crew executed successfully! Here are the results:\n{result}"
                ).send()
            except Exception as e:
                await cl.Message(content=f"An error occurred: {e}").send()
    except Exception as e:
        await cl.Message(content=f"An error occurred while processing your request: {e}").send()
