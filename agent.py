import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Model used for analysis. Kept as a constant so it's easy to swap out.
MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

# File types this agent currently knows how to handle.
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}

# The agent's "job description". This shapes how it behaves for every request.
INSTRUCTIONS = """
You are an AI file analysis assistant.

First understand what type of information the uploaded file contains.

If the file is a research paper:
- Identify the research question.
- Explain the methodology.
- Summarize the results.
- Explain the conclusion.
- Identify limitations.

If the file contains tabular data:
- Identify the columns.
- Describe important patterns.
- Identify unusual values when possible.
- Explain trends clearly.
- Do not invent numerical results.

If the file is a general document:
- Identify its main purpose.
- Summarize the important sections.
- Answer questions using information from the document.

Always:
- Use the file as your primary source.
- Do not invent facts.
- Clearly distinguish facts from inferences.
- Say when the file does not contain enough information.
- Use simple language unless the user asks for technical language.
- Use bullet points when they make the answer easier to understand.
"""


def get_file_path() -> str:
    """Ask the user for a file path and make sure it exists and is supported."""
    file_path = input("Enter the path to your file: ").strip()

    if not os.path.exists(file_path):
        print("File not found.")
        raise SystemExit(1)

    extension = os.path.splitext(file_path)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        print(f"Unsupported file type: {extension}")
        print("Supported types:", ", ".join(sorted(ALLOWED_EXTENSIONS)))
        raise SystemExit(1)

    return file_path


def upload_file(client: OpenAI, file_path: str):
    """Upload the file to OpenAI and return the uploaded file object."""
    try:
        with open(file_path, "rb") as file:
            uploaded_file = client.files.create(
                file=file,
                purpose="user_data",
            )
        return uploaded_file
    except Exception as error:
        print("The file could not be uploaded.")
        print(error)
        raise SystemExit(1) from error


def ask_agent(client: OpenAI, uploaded_file_id: str, question: str) -> str:
    """Send a question + the uploaded file to the model and return its answer."""
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": question},
                    {"type": "input_file", "file_id": uploaded_file_id},
                ],
            }
        ],
    )
    return response.output_text


def main() -> None:
    client = OpenAI()

    file_path = get_file_path()
    uploaded_file = upload_file(client, file_path)
    print(f"\nSuccessfully uploaded: {os.path.basename(file_path)}")

    print("\nYour file is ready to analyze.")
    print("Ask questions about the file.")
    print("Type 'exit' when you are finished.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer = ask_agent(client, uploaded_file.id, question)
            print("\nAgent:")
            print(answer, "\n")
        except Exception as error:
            print("\nThe agent encountered an error.")
            print(error, "\n")


if __name__ == "__main__":
    main()
