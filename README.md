# AI File Analysis Agent

A command-line AI agent, built in Python with the OpenAI Responses API, that lets you upload a file (PDF, TXT, DOCX, or CSV) and ask natural-language questions about it — no separate function needed for every possible question.

## Features

- Upload a file from your computer and send it directly to the model
- Ask unlimited follow-up questions in a chat loop (no restarting the script)
- File-type validation (`.pdf`, `.txt`, `.docx`, `.csv`)
- Clear, extensible agent instructions that adapt to research papers, tabular data, or general documents
- Basic error handling around uploads and API calls
- API key kept out of source code via environment variables / `.env`

## Project structure

```
file-analysis-agent/
├── agent.py            # Main application
├── requirements.txt    # Python dependencies
├── .env.example         # Template for your API key
├── .gitignore
└── README.md
```

## Setup

1. **Clone the repo**

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # macOS/Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your OpenAI API key**

   Copy the example env file and fill in your real key:

   ```bash
   cp .env.example .env
   ```

   Then edit `.env`:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

   Get a key from your [OpenAI developer account](https://platform.openai.com/api-keys). Never commit your real `.env` file — it's already covered by `.gitignore`.

## Usage

```bash
python agent.py
```

You'll be prompted for a file, then you can ask as many questions as you like:

```
Enter the path to your file: research.pdf

Successfully uploaded: research.pdf

Your file is ready to analyze.
Ask questions about the file.
Type 'exit' when you are finished.

You: What is the main argument of this paper?

Agent:
...

You: exit
Goodbye!
```

## How it works

1. Python checks that the file exists and has a supported extension.
2. The file is uploaded via `client.files.create(..., purpose="user_data")`, which returns a file ID.
3. Each question is sent to `client.responses.create(...)` along with that file ID and a set of instructions describing the agent's role.
4. The model's answer (`response.output_text`) is printed back to the terminal.

```text
Open file → Upload file → Get file ID → Send question + file ID → Model analyzes file → Print answer
```

## Ideas for extending this project

- **RAG / vector search** for very large document collections (search first, then send only the relevant chunks)
- **Analysis modes** (summarize / explain / analyze) selectable by the user
- **Web UI** with FastAPI or Flask instead of the terminal
- **Function calling / tools** so the agent can run code, search the web, or query a database

## Security notes

- Never hard-code your API key in source files.
- Keep `.env` out of version control (already handled by `.gitignore`).
- Be careful uploading sensitive files (medical, financial, or confidential documents) — review your data-handling and retention needs before processing sensitive data with any third-party API.

