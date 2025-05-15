**UNE Support Agent Documentation**

# Responsible AI Multi Agent UNE Support Bot

This project is a responsible AI Multi Agent chatbot designed to assist students and staff at the **University of New England (UNE)** in **Armidale, Australia**. It uses **OpenAI Agents SDK** to enable multi-agent LLM orchestration for course related advices, poetry generation on life at UNE, and schedule inquiries on classes at UNE.

> **Note:** We use the **OpenAI Agents SDK** as **OpenAI Swarms framework is deprecated and has been replaced by Open AI Agents SDK**.

---

## Special Features

### Multi-Agent Framework
- **Triage Agent**: Directs questions to the correct agent.
- **Course Assistant Agent**: Handles course-related questions.
- **Schedule Assistant Agent**: Assists with class timings and academic calendars.
- **Poetry Assistant Agent**: Generates creative responses like poems.

### Responsible AI Capabilities
- **Anonymization**: Sensitive info in user input is detected and removed to protect privacy of the users.
- **Content Filtering**:
  - Input guardrails for **restricting content generation for user inputs with bad words**.
  - Output guardrails for **restricting excessively long responses**.
- **Prompt Engineering**:
  - All references to "UNE" or "University" are assumed to refer to **UNE, Armidale** only.
  - Rejects queries not related to UNE.

### Logging
- Log files are organized by environment:
  - `dev`, `qa`, and `prod` have separate log paths.
- Supports future remote logging server setup.

### Frontend UI
- Simple UI HTML/CSS/JavaScript.
- Includes UNE branding and loading animation.

---

## Steps to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/isharabnd001/UNE_support_agent.git
cd UNE_support_agent
```
### 2. Create a Virtual Enviroment

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Dependencies

```bash
OPENAI_API_KEY=your_openai_api_key
DJANGO_ENV=dev
MAX_OUTPUT_WORDS=1000
```

### 5. Run Migrations and Start Server

```bash
python manage.py migrate
python manage.py runserver
```

## Steps to Run the TESTs Locally

```bash
python manage.py test
```

---

## Future Improvements

### 1. RAG (Retrieval-Augmented Generation)

Index UNE handbooks, policy docs,FAQs, etc and then use it as ground data for RAG to provide more accurate answers.

### 2. Authentication & Identity

Single Sign-On (SSO) with UNE’s internal identity provider for staff/students
OAuth 2.0 login for external users (e.g., Google, Microsoft)

### 3. Data Storage with Privacy

Secure chat history storage (non-viewable, encrypted) for users to retrieve context across sessions to improve multi-turn conversation

### 4. Voice Support Integrations

Integrate with Twilio Voice API and enabling speech-to-text transcription for real-time assistant queries via phone

### 5. Admin Tools to  Monitor

Build admin dashboard to monitor agent usage, guardrail triggers, and feedback for students/staff.
