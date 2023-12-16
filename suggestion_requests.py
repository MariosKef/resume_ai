import uuid
from openai import AsyncOpenAI
from typing import List
from dotenv import load_dotenv


load_dotenv()
client = AsyncOpenAI()


class SuggestionRequests:
    """
    Creates and submits the request to the openAI API and attaches a status and ID
    attribute to each request.
    """

    def __init__(self, cover_letter, job_description) -> None:
        """
        job_description: the job description
        cover_letter: the users cover letter
        request_status: the status of the request (Created/Processing/Finished)
        request_id: the unique ID of the request
        """
        self.job_description = job_description
        self.cover_letter = cover_letter
        self.request_status = "Created"
        self.request_id = str(uuid.uuid4())
        self.completion = None

    def concat_messages(self) -> List[dict]:
        """
        Concatenates the cover letter and the job description with the system messages.

        returns: concatenated messages
        TODO: check langchain
        TODO: move the below to another .py
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant working as a job recruiter.",
            },
            {
                "role": "user",
                "content": """Let me know if the following cover letter which is delimited
                    by double backslashes matches nicely the job description which
                    is delimited by angled braces (<).
                    First, create your own cover letter before making a decision.
                    In the end, let me know if my cover letter is suitable for the
                    job descriptions and suggest improvements. If nothing is missing
                    just say that it is suitable for the job description and no additions
                    are needed. Return the response in JSON format with a field 'Suitability'
                    for the decision and a field 'Improvements' for suggestions.
                    \n \\\ \n"""
                + self.cover_letter
                + "\n"
                + "\\\ \n"
                + "< \n"
                + self.job_description
                + "\n"
                + "<",
            },
        ]
        return messages

    @staticmethod
    def extract_message(result):
        """ """
        return result.choices[0].message.content

    async def generate_improvements(self):
        """
        Sends the request to the chat completion openAI API endpoint.
        Note: Only accepts the gpt-3.5-turbo-1106 model

        return:
        """

        messages = self.concat_messages()
        completion = await client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            response_format={"type": "json_object"},
        )
        self.request_status = "Finished"
        # TODO: put the update in another function
        self.completion = self.extract_message(completion)
        print(f"completion: {self.completion}")
        # self.completion = f'{{\n  "Suitability": "{self.cover_letter}",\n  "Improvements": "{self.job_description}"}}'
