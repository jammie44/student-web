# StudentHub - AI Powered Student Productivity Platform

A comprehensive SaaS platform for students featuring AI-powered tools for CV generation, assignment formatting, research summarization, plagiarism detection, and more.

## Features

- **AI CV Generator**: Create professional CVs with AI assistance
- **Assignment Formatting Tool**: Format assignments professionally
- **Research Summarization**: Summarize research papers and documents
- **Plagiarism Detection**: Check text for plagiarism
- **AI Study Assistant**: Get help with studying and questions
- **PDF Tools**: Upload and query research documents
- **User Management**: Registration, login, and admin dashboard
- **Credit System**: Subscription-based AI usage tracking

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite
- **AI**: OpenAI GPT-4o-mini, FAISS vector search
- **Frontend**: HTML, TailwindCSS, Vanilla JavaScript
- **Authentication**: JWT tokens
- **Vector Storage**: FAISS for document embeddings

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd student-web
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Run the application:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

6. Open your browser to `http://localhost:8000` for the API, and open `frontend/login.html` for the frontend.

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
student-web/
├── backend/
│   ├── app/
│   │   ├── core/          # Configuration, database, security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic services
│   │   ├── vector_store/  # FAISS vector storage
│   │   ├── api/v1/endpoints/  # API endpoints
│   │   └── tasks/         # Background tasks
├── frontend/              # HTML frontend
├── vector_store/          # FAISS indices
├── uploads/               # Uploaded files
├── alembic/               # Database migrations
└── requirements.txt       # Python dependencies
```

## Usage

1. Register a new account or login
2. Use the dashboard to access various AI tools
3. Upload research documents for RAG-based Q&A
4. Monitor usage and credits

## Development

- Backend API runs on `http://localhost:8000`
- Frontend is static HTML served from `frontend/`
- Database is SQLite (`studenthub.db`)
- Vector store uses FAISS for embeddings

## License

MIT License