import argparse
import logging
from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import AsyncOpenAI
from collections import defaultdict
from suggestion_request import SuggestionRequest

load_dotenv()
client = AsyncOpenAI()

app = Flask(__name__)
requests = defaultdict(int)


@app.route("/requests", methods=["POST"])
async def submit_suggestion():
    # Get your necessary data to make a new request
    cover_letter = request.json["cover-letter"]
    job_description = request.json["job-description"]

    app.logger.debug(f"cover letter: {cover_letter}")
    app.logger.debug(f"job: {job_description}")
    my_request = SuggestionRequest(cover_letter, job_description)
    requests[my_request.request_id] = my_request
    my_request.start()

    return {"request_id": my_request.request_id}


@app.route("/requests/<request_id>", methods=["GET"])
def get_suggestion(request_id):
    # Your frontend knows the request id, it can use it to retrieve the status + data if there
    app.logger.debug(requests)
    return requests[request_id].to_json()


@app.route("/", methods=["GET", "POST"])
def index():
    # Returns landing page.
    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="log_level",
        const=logging.INFO,
        default=logging.WARNING,
    )
    group.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="log_level",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    args = parser.parse_args()
    app.logger.setLevel(args.log_level)

    app.run(debug=args.log_level == logging.DEBUG)


## API call tp openaiAPI does not work twice unless restarting
