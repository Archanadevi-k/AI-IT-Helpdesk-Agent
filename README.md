# AI IT Helpdesk Agent

An AI/ML-powered IT support assistant that automatically analyzes IT support tickets, predicts their category and priority, retrieves relevant knowledge-base articles, and drafts support responses.

## Project Overview

 The **AI IT Helpdesk Agent** is designed to reduce repetitive manual work in IT support operations.

When an employee submits an IT issue, the system processes the ticket using **Natural Language Processing (NLP)** and Machine Learning techniques. It identifies the type of issue, estimates its priority, finds the most relevant troubleshooting article, and generates a draft response for the support team.

The application is built with **Python and Streamlit** and runs locally without requiring an external API key.

## Objectives

* Automate IT ticket classification
* Predict ticket priority based on urgency and impact
* Retrieve relevant troubleshooting information
* Generate draft responses for IT support staff
* Maintain ticket history and status
* Demonstrate practical application of AI/ML in IT support

## Key Features

### &#x20;Ticket Analysis

Users can submit an IT issue through the Streamlit interface.

The system automatically provides:

* Ticket category
* Priority level
* Prediction confidence
* AI analysis/reason
* Recommended knowledge-base article
* Draft support response
* Unique ticket ID

### AI-Based Classification

The system classifies tickets into categories such as:

* Network
* Hardware
* Software
* Account & Access
* Email
* Security
* Other

The classification pipeline uses **TF-IDF feature extraction** with **Logistic Regression**.

### Priority Prediction

Tickets are assigned one of four priority levels:

* **Critical**
* **High**
* **Medium**
* **Low**

Priority is determined using detected urgency, service-disruption, security, and business-impact signals.

### Knowledge Base Retrieval

The system searches the internal FAQ/knowledge base and retrieves the most relevant troubleshooting article using:

* TF-IDF
* Cosine Similarity

### &#x20;Response Drafting

Based on the ticket category, priority, and recommended knowledge article, the system generates a draft response that an IT support engineer can review and send.

### Ticket History

Created tickets are stored in an SQLite database.

Support staff can:

* View previous tickets
* View ticket details
* Check category and priority
* View confidence
* Update ticket status

Available statuses:

`Open` → `In Progress` → `Resolved` → `Closed`

### Explainability

The application displays detected signals and classification information so users can understand the factors considered when assigning a category and priority.

## System Architecture

```text
Employee / User
      │
      ▼
Submit IT Issue
      │
      ▼
Text Cleaning & NLP
      │
      ├───────────────┐
      ▼               ▼
Category Prediction   Priority Prediction
(TF-IDF + LR)         (Rule-Based Signals)
      │               │
      └───────┬───────┘
              ▼
       Knowledge Retrieval
       (TF-IDF + Cosine Similarity)
              │
              ▼
       Response Drafting
              │
              ▼
       SQLite Ticket Storage
              │
              ▼
       Streamlit Dashboard
```

## Technology Stack

| Technology          | Purpose                   |
| ------------------- | ------------------------- |
| Python              | Core programming language |
| Streamlit           | Web application interface |
| Scikit-learn        | Machine Learning          |
| TF-IDF              | Text feature extraction   |
| Logistic Regression | Ticket classification     |
| Cosine Similarity   | Knowledge retrieval       |
| Pandas              | Data processing           |
| NumPy               | Numerical operations      |
| SQLite              | Ticket storage            |
| Pytest              | Automated testing         |
| GitHub Actions      | Continuous Integration    |

## Project Structure

```text
AI-IT-Helpdesk-Agent/
│
├── .github/
│   └── workflows/
│       └── python.yml
│
├── data/
│   ├── faqs.csv
│   └── sample_tickets.csv
│
├── src/
│   ├── __init__.py
│   ├── helpdesk.py
│   └── database.py
│
├── tests/
│   └── test_helpdesk.py
│
├── .gitignore
├── app.py
├── LICENSE
├── README.md
└── requirements.txt
```

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/Archanadevi-k/AI-IT-Helpdesk-Agent.git
cd AI-IT-Helpdesk-Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## &#x20;Run Tests

Run the automated tests using:

```bash
python -m pytest -q
```

Expected result:

```text
3 passed
```

The project also uses **GitHub Actions** to automatically run the test suite whenever changes are pushed to the repository.

## Application Workflow

```text
1. User submits an IT issue
          ↓
2. Ticket text is cleaned
          ↓
3. Category is predicted
          ↓
4. Priority is determined
          ↓
5. Relevant FAQ is retrieved
          ↓
6. Support response is drafted
          ↓
7. Ticket is stored in SQLite
          ↓
8. Support team reviews and manages the ticket
```

## AI/ML Approach

### Ticket Classification

The project uses:

**TF-IDF → Logistic Regression**

TF-IDF converts the ticket description into numerical text features. Logistic Regression then predicts the most appropriate support category.

### Knowledge Retrieval

The FAQ documents are converted into TF-IDF vectors. **Cosine Similarity** compares the submitted ticket with the available knowledge-base articles and selects the most relevant article.

### Priority Prediction

Priority prediction uses a lightweight rule-based approach that detects signals such as:

* Security incidents
* Urgent language
* Service disruption
* Broad business impact
* Production/system downtime

## Human-in-the-Loop

The system is designed as an **AI-assisted support tool**, not a fully autonomous IT administration system.

The AI provides recommendations and response drafts. High-impact actions such as:

* Account changes
* Access permission changes
* Password resets
* Device administration

remain under human control.

## Limitations

* The ML classifier uses a lightweight embedded training dataset.
* Priority prediction currently uses rule-based signals rather than a trained priority model.
* The knowledge base is stored in CSV format.
* The application does not directly integrate with enterprise ticketing platforms.
* Generated responses should be reviewed by support staff before being sent.
* The current application is intended as a demonstration/prototype rather than a production IT service-management system.

## Future Enhancements

Possible future improvements include:

* BERT/DistilBERT-based ticket classification
* RAG-based knowledge retrieval
* FAISS/vector database integration
* Larger real-world training datasets
* Multilingual support including English and Tamil
* SLA-aware priority prediction
* Jira/ServiceNow integration
* User authentication and role-based access
* IT support analytics dashboard
* Docker deployment
* Feedback-based model improvement

## Testing & CI

The project includes automated unit tests using **Pytest**.

GitHub Actions automatically executes the test suite on repository changes.

Current test status:

```text
✅ 3 tests passed
✅ GitHub Actions workflow passed
```

## &#x20;Project Information

This project demonstrates the practical application of:

* Artificial Intelligence
* Machine Learning
* Natural Language Processing
* Information Retrieval
* Database Management
* Streamlit Application Development
* Software Testing
* Git & GitHub
* Continuous Integration

## &#x20;Project Summary

> **AI IT Helpdesk Agent is an NLP-based AI assistant that classifies IT tickets, predicts their urgency, retrieves relevant troubleshooting knowledge, and drafts support responses, helping IT teams handle repetitive support requests more efficiently.**

## 👤 Author

**Archanadevi-k**

GitHub:

https://github.com/Archanadevi-k/AI-IT-Helpdesk-Agent

