import logging
from typing import Dict, Any, Optional
from datetime import datetime
import os

import google.generativeai as genai
import chromadb
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class NotebookLMService:
    """
    NotebookLM-style service wrapper.

    Keeps the same interface so agents do not change.
    """

    def __init__(self, api_key: Optional[str] = None):

        self.service_name = "NotebookLM"

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel("gemini-1.5-flash")

        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.db = chromadb.Client()
        self.collection = self.db.get_or_create_collection("knowledge")

    async def generate_summary(self, document_text: str) -> Dict[str, Any]:
        """
        Generate a summary grounded in document text.
        """

        try:

            prompt = f"""
            Summarize the following document clearly.

            Document:
            {document_text}
            """

            response = self.model.generate_content(prompt)

            return {
                "status": "success",
                "data": {
                    "summary": response.text,
                    "service": self.service_name
                },
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:

            logger.error("NotebookLM summary generation failed", exc_info=True)

            return {
                "status": "error",
                "error_code": "AI_SERVICE_FAILURE",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    async def extract_insights(self, document_text: str) -> Dict[str, Any]:
        """
        Extract insights from text.
        """

        try:

            prompt = f"""
            Extract the key insights from this document.

            {document_text}

            Return bullet points.
            """

            response = self.model.generate_content(prompt)

            insights = [
                line.strip("- ").strip()
                for line in response.text.split("\n")
                if line.strip()
            ]

            return {
                "status": "success",
                "data": {
                    "insights": insights,
                    "service": self.service_name
                },
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:

            logger.error("NotebookLM insight extraction failed", exc_info=True)

            return {
                "status": "error",
                "error_code": "AI_SERVICE_FAILURE",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    async def index_document(self, document_text: str):
        """
        Optional helper to store document chunks for retrieval.
        """

        chunks = [
            document_text[i:i+500]
            for i in range(0, len(document_text), 500)
        ]

        for chunk in chunks:
            embedding = self.embed_model.encode(chunk).tolist()

            self.collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[str(hash(chunk))]
            )

    async def query(self, question: str) -> str:
        """
        Ask a question grounded in stored documents.
        """

        query_embedding = self.embed_model.encode(question).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=4
        )

        context = "\n".join(results["documents"][0])

        prompt = f"""
        Answer the question using ONLY the context.

        Context:
        {context}

        Question:
        {question}
        """

        response = self.model.generate_content(prompt)

        return response.text