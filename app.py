# # from flask import Flask, request, jsonify, render_template
# # from dotenv import load_dotenv
# # import os
# # from langchain_experimental.agents import create_csv_agent
# # from langchain_openai import ChatOpenAI
# # from scripts.LLMScript import ReturnUserAnswer

# # # Load environment variables from .env file
# # load_dotenv()

# # app = Flask(__name__)

# # @app.route("/ask", methods=["POST"])
# # def ask():
# #     user_question = request.form["question"]
# #     query = """
# #         This CSV File Contains The data of The Hospital Patient.
# #         When a user asks a question, answer it in a clear and organized way, providing all the relevant information based on the Data into the Response i want to Show the Details into My Front End Side.
# #         If a user requests to see all patient details, display Each Detail Except Null OR empty Value. If any user ask you to give a phone number then you should give a number in string.
# #         you must answer the Question in Proper Sentence.
# #         """
# #     response = ReturnUserAnswer(query + user_question)
# #     print("Response :: ", response)
# #     return {"response": response}

# # if __name__ == "__main__":
# #     app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from langchain_experimental.agents import create_csv_agent
# from langchain_openai import ChatOpenAI


# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# def ReturnUserAnswer(userQuestion):
#     # Get API key from environment variables
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         return "API key not found in environment variables."
#     try:
#         # Create the agent with the OpenAI API key and the CSV file
#         agent = create_csv_agent(
#             ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key),
#             "./dataset/CleanData.csv",
#             verbose=True,
#         )
#         response = agent.invoke(userQuestion)  # Use invoke instead of run
#         return response["output"]
#     except FileNotFoundError:
#         return "CSV file not found. Please check the file path."
#     except Exception as e:
#         return f"Error Occurs: {str(e)}"

# @app.route('/query', methods=['POST'])
# def query():
#     data = request.json
#     question = data.get('question', '')
#     query = """
#     This CSV File Contains The data of The Hospital Patient.
#     When a user asks a question, answer it in a clear and organized way, providing all the relevant information based on the Data.
#     If a user requests to see all patient details, display Each Detail Except Null OR empty Value.
#     """
#     response = ReturnUserAnswer(query + question)
#     return jsonify({'response': response})


# @app.route("/ask", methods=["POST"])
# def ask():
#     user_question = request.form["question"]
#     query = """
#         This CSV File Contains The data of The Hospital Patient.
#         When a user asks a question, answer it in a clear and organized way, providing all the relevant information based on the Data into the Response i want to Show the Details into My Front End Side.
#         If a user requests to see all patient details, display Each Detail Except Null OR empty Value. If any user ask you to give a phone number then you should give a number in string.
#         you must answer the Question in Proper Sentence.
#         """
#     response = ReturnUserAnswer(query + user_question)
#     print("Response :: ", response)
#     return {"response": response}


# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, request, jsonify, render_template
# from dotenv import load_dotenv
# import os
# from langchain_experimental.agents import create_csv_agent
# from langchain_openai import ChatOpenAI
# from scripts.LLMScript import ReturnUserAnswer

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# @app.route("/ask", methods=["POST"])
# def ask():
#     user_question = request.form["question"]
#     query = """
#         This CSV File Contains The data of The Hospital Patient.
#         When a user asks a question, answer it in a clear and organized way, providing all the relevant information based on the Data into the Response i want to Show the Details into My Front End Side.
#         If a user requests to see all patient details, display Each Detail Except Null OR empty Value. If any user ask you to give a phone number then you should give a number in string.
#         you must answer the Question in Proper Sentence.
#         """
#     response = ReturnUserAnswer(query + user_question)
#     print("Response :: ", response)
#     return {"response": response}

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from werkzeug.utils import secure_filename
import pandas as pd

# Load environment variables from .env file
# load_dotenv()

app = Flask(__name__)
CORS(app)

# ===================
# gpt-3.5-turbo-1106
# ===================

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
last_uploaded_file = None

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def ReturnUserAnswer(userQuestion):
    # Get API key from environment variables
    # api_key = os.getenv("OPENAI_API_KEY")
    # if not api_key:
    #     return "API key not found in environment variables."

    # if not last_uploaded_file:
    #     return "No CSV file uploaded yet."

    try:
        # Create the agent with the OpenAI API key and the uploaded CSV file
        agent = create_csv_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106", api_key="sk-proj-TXXyzfrcydLc0v8r6tQlT3BlbkFJ8y4eAz6z8Hp41Me6fM1L"),
            last_uploaded_file,
            verbose=True,
        )
        response = agent.invoke(userQuestion)  # Use invoke instead of run
        return response["output"]
    except FileNotFoundError:
        return "CSV file not found. Please check the file path."
    except Exception as e:
        return f"Error Occurs: {str(e)}"

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question", "")
    query = """
        This CSV File Contains The data of The Hospital Patient.
        When a user asks a question, answer it in a clear and organized way, providing all the relevant information based on the Data into the Response Variable not inside the terminal.
        If a user requests to see all patient details, display Each Detail Except Null OR empty Value. If any user ask you to give a phone number then you should give a number in string.
        you must answer the Question in Proper Sentence.
    """
    response = ReturnUserAnswer(query + question)
    print("Response  ::  ", response)
    return jsonify({"response": response})

@app.route("/upload", methods=["POST"])
def upload_file():
    global last_uploaded_file

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Delete the last uploaded file if it exists
        if last_uploaded_file and os.path.exists(last_uploaded_file):
            os.remove(last_uploaded_file)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        last_uploaded_file = filepath  # Update the last uploaded file path
        return jsonify({"message": "Successfully Uploaded"}), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
