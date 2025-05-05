import asyncio
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from browser_use.agent.service import Agent
from browser_use.controller.service import Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr, BaseModel
from langchain.callbacks import get_openai_callback

logging.basicConfig(level=logging.INFO)

class CheckResultStatus(BaseModel):
    launchedBrowser: str
    title: str
    titleValidation: str
    status: str
    numberOfActions: str
    NumberOfFileorTest: str
    message: str
    sucess: str

controller = Controller(output_model=CheckResultStatus)

def estimate_tokens(text):
    return len(text)

async def site_validation():
    try:
        # Read the task from an external text file
        with open('task.txt', 'r') as file:
            task = file.read().strip()

        api_key = os.environ["GOOGLE_API_KEY"]
        os.environ["GEMINI_API_KEY"] = ""
        logging.info("API key loaded")
        llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(api_key))
        logging.info("LLM initialized")
        agent = Agent(task=task, llm=llm, controller=controller, use_vision=True)
        logging.info("Agent created")
        history = await agent.run()
        history.save_to_file('agentRun.json')
        logging.info("Agent run completed")
        test_result = history.final_result()
        validate_data = CheckResultStatus.model_validate_json(test_result)

        # Generate HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Site Validation Report</title>
        </head>
        <body>
            <h1>Site Validation Report</h1>
            <p><strong>Task:</strong> {task}</p>
            <p><strong>Launched Browser:</strong> {validate_data.launchedBrowser}</p>
            <p><strong>Title:</strong> {validate_data.title}</p>
            <p><strong>Title Validation:</strong> {validate_data.titleValidation}</p>
            <p><strong>Status:</strong> {validate_data.status}</p>
            <p><strong>Number of Files or Tests:</strong> {validate_data.NumberOfFileorTest}</p>
            <p><strong>Number of Actions:</strong> {validate_data.numberOfActions}</p>
            <p><strong>Message:</strong> {validate_data.message}</p>
            <p><strong>Success:</strong> {validate_data.sucess}</p>
        </body>
        </html>
        """

        # Write HTML to a file
        with open('result.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        print("HTML report generated: result.html")

        # Token usage estimate
        input_tokens = estimate_tokens(task)
        output_tokens = estimate_tokens(test_result)
        total_tokens = input_tokens + output_tokens

        print(f"\n📊 Token Usage Estimate:")
        print(f"Prompt Tokens: {input_tokens}")
        print(f"Response Tokens: {output_tokens}")
        print(f"Total Estimated Tokens: {total_tokens}")

    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(site_validation())
