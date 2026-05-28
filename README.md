# AI App Compiler

A compiler-inspired AI system that converts natural language product requirements into structured, validated, and executable full-stack application configurations.

The system transforms user prompts into:

* Intent IR
* Architecture IR
* Database Schema
* API Schema
* UI Schema
* SQLAlchemy Models
* FastAPI Routes
* React Components

The platform includes:

* multi-stage generation pipeline
* schema validation
* automated repair engine
* runtime execution
* evaluation framework
* deterministic structured generation

---

# Problem Statement

Modern LLMs can generate code, but they often produce:

* inconsistent outputs
* hallucinated fields
* invalid schemas
* broken API contracts
* non-executable systems

This project approaches AI software generation as a:

# compiler + systems engineering problem

instead of a simple prompting task.

---

# System Architecture

Pipeline:


Natural Language Prompt
        ↓
Intent Extraction
        ↓
Architecture Generation
        ↓
Database Schema Generation
        ↓
API Schema Generation
        ↓
UI Schema Generation
        ↓
Validation Engine
        ↓
Repair Engine
        ↓
Code Generation
        ↓
Runtime Execution


---

# Features

## Multi-Stage Generation Pipeline

* Intent extraction
* Architecture planning
* Schema generation
* Runtime code generation

## Validation + Repair Engine

Automatically detects:

* missing CRUD endpoints
* invalid entities
* schema inconsistencies
* API/DB mismatches
* role mismatches

Automatically repairs:

* missing APIs
* incomplete CRUD
* analytics endpoints
* schema inconsistencies

## Runtime Code Generation

Generates:

* SQLAlchemy models
* FastAPI routes
* React pages

## Execution Awareness

Generated output is executable using:

* FastAPI backend
* React frontend
* runtime integration

## Evaluation Framework

Supports:

* automated testing
* latency tracking
* repair metrics
* success rate analysis

---

# Tech Stack

## Backend

* FastAPI
* Python
* Pydantic
* SQLAlchemy

## Frontend

* React
* Vite
* Tailwind CSS
* Axios

## AI Layer

* OpenRouter API
* DeepSeek Models

---

# Example Prompt


Build a CRM with login, contacts, analytics dashboard,
role-based access and subscriptions.


---

# Generated Outputs

The system generates:

## Intent IR


{
  "app_name": "CRM",
  "features": ["login", "analytics"]
}


## API Schema


{
  "path": "/contacts",
  "method": "GET"
}


## SQLAlchemy Models


class Contact(Base):
    __tablename__ = "contacts"


---

# Evaluation Framework

The project includes:


app/evaluation/run_evaluation.py


Evaluation tracks:

* success rate
* latency
* repair success
* failure handling

Test dataset includes:

* production-style prompts
* vague prompts
* incomplete prompts
* conflicting prompts

---

# Reliability Mechanisms

The system enforces:

* strict JSON structure
* cross-layer consistency
* deterministic schemas
* validation contracts
* targeted repair instead of blind retries

---

# How To Run

## Backend


pip install -r requirements.txt
uvicorn app.main:app --reload


## Frontend


cd frontend
npm install
npm run dev


Frontend:

http://localhost:5175


Backend:


http://127.0.0.1:8000




# Project Structure


app/
 ├── pipeline/
 ├── runtime/
 ├── schemas/
 ├── evaluation/
 ├── generated/
 ├── main.py

frontend/
 ├── src/
 ├── pages/
 ├── components/



# Tradeoffs

## Quality vs Latency

* multi-stage generation improves consistency
* increases latency slightly

## Determinism vs Creativity

* strict schemas improve reliability
* reduce output randomness

## Repair vs Full Regeneration

* targeted repair is cheaper and faster
* avoids cascading failures



# Future Improvements

* ZIP export of generated projects
* Monaco editor integration
* visual architecture graphs
* deployment automation
* multi-framework support
* agentic planning


# Conclusion

This project demonstrates how LLMs can be controlled using:

* compiler-inspired pipelines
* validation systems
* structured intermediate representations
* deterministic schema enforcement
* runtime-aware execution

instead of relying on single-prompt generation.
