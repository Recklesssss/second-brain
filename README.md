# AI Second Brain Platform

An integrated frontend and backend system for autonomous knowledge management and AI-driven learning.

## Architecture

- **Backend**: FastAPI with Pydantic models for type safety
- **Frontend**: React with Vite, ShadCN UI components
- **Database**: Neo4j knowledge graph (planned)
- **AI Integration**: Gemini and NotebookLM services

## Features

### Input Methods
- **Domain Creation**: Add new knowledge domains
- **Learning Modules**: Create structured learning content
- **Research**: Explore concepts with AI assistance

### Multi-Agent System
- Research Agent
- Learning Agent
- Question Generator
- Idea Synthesizer
- Curriculum Builder
- Thinking Engine
- Planning Engine

## Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Neo4j (optional, for full functionality)

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the backend
python run_backend.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup
```bash
cd second_brain_ai/frontend/cognitive-synthesis-engine

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Domains
- `POST /api/domains` - Create a new domain
- `GET /api/domains` - List all domains
- `GET /api/domains/{id}` - Get domain by ID

### Learning
- `POST /api/learning/module` - Create a learning module
- `GET /api/learning/modules` - List learning modules
- `GET /api/learning/modules/{id}` - Get learning module by ID

### Research
- `POST /api/research/explore` - Research a concept
- `GET /api/research/results` - List research results
- `GET /api/research/results/{id}` - Get research result by ID

## Development

### Testing
```bash
# Run backend tests
pytest

# Run frontend tests
npm test
```

### Architecture Decisions
See ADR documents for key design decisions that guide development.

## Deployment

The system is designed for local development with plans for containerized deployment.