from fastapi import APIRouter, UploadFile, File, Depends, Form
from backend.app.services.document_processor import process_pdf, chunk_text
from backend.app.services.embedding_service import get_embedding
from backend.app.vector_store.faiss_store import faiss_store
from backend.app.services.rag_service import retrieve_relevant_chunks, generate_answer
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.research_document import ResearchDocument
from backend.app.models.document_chunk import DocumentChunk
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    text = process_pdf(file_path)
    # save document to db
    doc = ResearchDocument(user_id=current_user.id, filename=file.filename, file_path=file_path, content=text)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        faiss_store.add_embedding(embedding, chunk)
        # save chunk to db
        chunk_db = DocumentChunk(document_id=doc.id, chunk_text=chunk, embedding=embedding, chunk_index=i)
        db.add(chunk_db)
    db.commit()
    faiss_store.save()
    return {"message": "Document uploaded and processed"}

@router.post("/ask")
def ask_question(query: str = Form(...), current_user: User = Depends(get_current_user)):
    chunks = retrieve_relevant_chunks(query)
    context = " ".join(chunks)
    answer = generate_answer(query, context)
    return {"answer": answer}

@router.post("/summarize")
def summarize_research_endpoint(text: str, current_user: User = Depends(get_current_user)):
    from backend.app.services.ai_service import summarize_research
    summary = summarize_research(text)
    return {"content": summary}