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
from langchain_openai import ChatOpenAI
from pydantic import SecretStr, BaseModel

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
    screenshots: str


controller = Controller(output_model=CheckResultStatus)


async def site_validation():
    try:
        # List of task files
        task_files = ['task1.txt']  # Add your task file names here

        # Initialize combined HTML content
        combined_html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Combined Site Validation Report</title>
        </head>
        <body>
            <h1>Combined Site Validation Report</h1>
        """

        for task_file in task_files:
            # Read the task from each text file
            with open(task_file, 'r') as file:
                task = file.read().strip()

            api_key = os.environ["OPENAI_API_KEY"]
            os.environ["OPEN_API_KEY"] = ""
            logging.info(f"API key loaded for task file: {task_file}")
            llm = ChatOpenAI(model='gpt-3.5-turbo', api_key=SecretStr(api_key))
            logging.info("LLM initialized")
            agent = Agent(task=task, llm=llm, controller=controller, use_vision=False)
            logging.info(f"Agent created for task file: {task_file}")
            history = await agent.run()
            history.save_to_file(f'agentRun_{task_file}.json')
            logging.info(f"Agent run completed for task file: {task_file}")
            test_result = history.final_result()
            validate_data = CheckResultStatus.model_validate_json(test_result)
# Save screenshot
         # Append each task's report to the combined HTML content
            combined_html_content += f"""
            <h2>Report for Task File: {task_file}</h2>
            <p><strong>Task:</strong> {task}</p>
            <p><strong>Launched Browser:</strong> {validate_data.launchedBrowser}</p>
            <p><strong>Title:</strong> {validate_data.title}</p>
            <p><strong>Title Validation:</strong> {validate_data.titleValidation}</p>
            <p><strong>Status:</strong> {validate_data.status}</p>
            <p><strong>Number of Files or Tests:</strong> {validate_data.NumberOfFileorTest}</p>
            <p><strong>Number of Actions:</strong> {validate_data.numberOfActions}</p>
            <p><strong>Message:</strong> {validate_data.message}</p>
            <p><strong>Success:</strong> {validate_data.sucess}</p>
            <p><strong>Screenshot:</strong></p>
       
            <hr>
            """

        # Close the combined HTML structure
        combined_html_content += """
        </body>
        </html>
        """

        # Write the combined HTML to a file
        combined_html_file_name = 'combined_result.html'
        with open(combined_html_file_name, 'w', encoding='utf-8') as html_file:
            html_file.write(combined_html_content)

        print(f"Combined HTML report generated: {combined_html_file_name}")

    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")



asyncio.run(site_validation())
# asyncio.run(send_email('result.html'))