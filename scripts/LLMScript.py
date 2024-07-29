from langchain_experimental.agents import create_csv_agent
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

def ReturnUserAnswer(userQuestion):
    # Get API key from environment variables
    api_key = os.getenv("OPENAI_API_KEY")

    print(f"API Key: {api_key}")

    if not api_key:
        return "API key not found in environment variables."
    try:
        # Create the agent with the OpenAI API key and the CSV file
        agent = create_csv_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key),
            ".\dataset\CleanData.csv",
            verbose=True,
            # agent_type=AgentType.OPENAI_FUNCTIONS,
        )

        response = agent.invoke(userQuestion)  # Use invoke instead of run
        # print("Response  :: ", response)
        return response["output"]
    except FileNotFoundError:
        return "CSV file not found. Please check the file path."
    except Exception as e:
        return "Error Occurs...!" + e

query = """
    This CSV File Contains The data of The Hospital Patient. When a user asks a question, answer it in a clear and organized way, providing all the relevant information based on the Data into the Response i want to Show the Details into My Front End Side. If a user requests to see all patient details, display Each Detail Except Null OR empty Value. If any user ask you to give a phone number then you should give a number in string. you must answer the Question in Proper Sentence.
"""

# Define the question
# provide me teh Details of the inquiry id 1, 2 and 3.
# provide me Name of the patient Whoes Inquiry is 12772, 12773,12774
# Give me the details of the inquiry, which are from Ahmadabad, have thyroid, and are 40 or older.

question = "provide me name of the inquiry who live in Jaipur"

# Get the response
response = ReturnUserAnswer(query + question)
print("Response :: ", response)
