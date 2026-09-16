# AI IT Helpdesk Agent

An internship-ready AI/ML project that automatically analyzes IT support tickets, predicts the ticket category and priority, retrieves a relevant knowledge-base article, and drafts a response for the support team.

## Project Name

**AI IT Helpdesk Agent — Intelligent Ticket Classification, Priority Prediction & Knowledge Retrieval**

## Problem Statement

IT helpdesks receive repetitive natural-language requests such as Wi-Fi problems, password issues, application errors, hardware failures and suspicious emails. Manually categorizing, prioritizing and answering every ticket takes time and can create inconsistent responses.

This project builds a lightweight AI assistant that:

1. Understands the text of an IT ticket.
2. Predicts its support category.
3. Estimates priority from urgency and impact signals.
4. Retrieves the most relevant troubleshooting article.
5. Generates a human-reviewable response draft.
6. Displays confidence and reasoning signals.

## Architecture

```text
User Ticket
    |
    v
Text Cleaning
    |
    +--------------------+
    |                    |
    v                    v
ML Classifier       Priority Rules
TF-IDF + LR         urgency/impact
    |                    |
    +---------+----------+
              |
              v
      Knowledge Retrieval
      TF-IDF + Cosine Similarity
              |
              v
       Response Drafting
              |
              v
       Streamlit Dashboard
```

## Technology Stack

- Python
- Streamlit
- Pandas / NumPy
- Scikit-learn
- TF-IDF vectorization
- Logistic Regression
- Cosine similarity
- CSV-based knowledge base

## Main Features

### 1. Ticket Classification
The NLP classifier predicts:
- Network
- Hardware
- Software
- Account & Access
- Email
- Security
- Other

### 2. Priority Prediction
The priority engine looks for urgency and business-impact signals and returns:
- Critical
- High
- Medium
- Low

### 3. Knowledge Retrieval
A TF-IDF retrieval system compares the ticket against the knowledge base and recommends the closest article.

### 4. Response Drafting
The system creates a support response containing the category, priority and recommended troubleshooting guidance.

### 5. Explainability
The interface exposes:
- classification confidence
- top category scores
- detected priority factors
- FAQ similarity score

## Folder Structure

```text
ai_it_helpdesk_agent/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── faqs.csv
│   └── sample_tickets.csv
└── src/
    ├── __init__.py
    └── helpdesk.py
```

## How to Run on Windows

### Step 1 — Install Python

Install Python 3.10+ from the official Python website and make sure **Add Python to PATH** is selected during installation.

Verify:

```bash
python --version
```

### Step 2 — Download / clone the project

If using Git:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai_it_helpdesk_agent
```

Or download the ZIP from GitHub and extract it.

### Step 3 — Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, Command Prompt can be used:

```cmd
.venv\Scripts\activate
```

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Start the application

```bash
streamlit run app.py
```

The terminal will show a local address, normally:

```text
http://localhost:8501
```

Open that address in Chrome or Edge.

## How to Run on macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## GitHub Upload

From the project folder:

```bash
git init
git add .
git commit -m "Initial commit - AI IT Helpdesk Agent"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do not upload passwords, API keys, company credentials, real employee information, or confidential tickets.

## Demo Inputs

Try these in the application:

**Network**
> I cannot connect my laptop to the office Wi-Fi.

**Account**
> I forgot my password and my account is locked.

**Security**
> I received a suspicious email asking me to verify my password.

**Hardware**
> My printer is not printing anything.

**Software**
> The application crashes every time I open it.

**High-impact**
> Our whole team cannot access the VPN and we have an important meeting soon.

## Machine Learning Approach

### Classification

The project uses TF-IDF features with unigram and bigram terms. Logistic Regression maps the ticket text to an IT-support category.

### Retrieval

The knowledge base is transformed into TF-IDF vectors. Cosine similarity is used to find the article closest to the submitted ticket.

### Priority

Priority is a transparent rule-based layer. Terms indicating security incidents, broad impact or service disruption increase the priority level.

This hybrid design is intentional: ML handles language classification and retrieval, while explicit rules make urgent/security escalation easier to inspect.

## Limitations

This is an internship/demo system rather than a production service desk.

- The classifier uses a small embedded training set.
- Priority rules are not a substitute for an organization's official SLA.
- The knowledge base is a CSV file.
- No real ticketing-system integration is included.
- The generated response should be reviewed by a human.
- The system must not be given secrets such as passwords or MFA codes.

## Future Enhancements

- Replace the small training set with an approved historical ticket dataset.
- Add BERT/DistilBERT fine-tuning for classification.
- Add an embedding/vector database such as FAISS.
- Add RAG with an approved internal document store.
- Add multilingual support for English/Tamil.
- Add ticket database and authentication.
- Integrate Jira, ServiceNow or another approved ticketing platform.
- Add SLA-aware priority prediction.
- Add feedback learning from support engineers.
- Add analytics for ticket volume, category trends and resolution time.
- Deploy with Docker and a production web server.

## Suggested Internship Viva Explanation

**One-line explanation:**

> "AI IT Helpdesk Agent is an NLP-based assistant that classifies IT tickets, predicts their urgency, retrieves relevant troubleshooting knowledge and drafts a response so that support engineers can handle repetitive requests faster."

**Why AI/ML?**

> "The ticket arrives as unstructured natural language. TF-IDF converts the text into numerical features and Logistic Regression predicts the support category. A second TF-IDF representation and cosine similarity retrieve the most relevant knowledge-base article."

**Why hybrid AI instead of only an LLM?**

> "For an internship prototype, a lightweight and explainable local model avoids API cost and protects ticket data. An LLM/RAG layer can be added later when organizational security and data policies allow it."

## License

Educational / internship project. Adapt the license and organization-specific policies before production use.
