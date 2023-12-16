from flask import Flask, render_template, request
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI
from collections import defaultdict
from suggestion_requests import SuggestionRequests

load_dotenv()
client = AsyncOpenAI()

app = Flask(__name__)
requests = defaultdict(int)


# Function to generate improvements based on user input using gpt-3.5-turbo
async def generate_improvements(cover_letter, job_description):
    print("booom")
    completion_requests = SuggestionRequests(
        cover_letter=cover_letter, job_description=job_description
    )
    requests[completion_requests.request_id] = {"data": vars(completion_requests)}

    print(f"completion request: {vars(completion_requests)}")
    await completion_requests.generate_improvements()
    requests[completion_requests.request_id].update({"data": vars(completion_requests)})
    return vars(completion_requests)


@app.route("/requests", methods=["POST"])
async def submit_suggestion():
    # Get your necessary data to make a new request
    cover_letter = request.json["cover-letter"]
    job_description = request.json["job-description"]

    print(f"cover letter: {cover_letter}")
    print(f"job: {job_description}")
    response = asyncio.create_task(generate_improvements(cover_letter, job_description))
    response = await response
    print(response)
    print("\n")

    return response


@app.route("/requests/<request_id>", methods=["GET"])
def get_suggestion(request_id):
    # Your frontend knows the request id, it can use it to retrieve the status + data if there
    print(requests)
    return requests[request_id]["data"]


@app.route("/", methods=["GET", "POST"])
def index():
    # Returns landing page.
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


## API call tp openaiAPI does not work twice unless restarting
