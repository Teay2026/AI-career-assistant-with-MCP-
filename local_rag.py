import os
import re
from typing import List, Dict

class SimpleRAG:
    """Simple keyword-based RAG system without heavy dependencies"""

    def __init__(self):
        self.documents = self._get_sample_skills()

    def _get_sample_skills(self) -> List[Dict[str, str]]:
        """Sample CV skills data"""
        return [
            {
                "id": "programming",
                "content": "Python programming with 3 years experience in web development, FastAPI, Django",
                "keywords": ["python", "web", "development", "fastapi", "django", "programming"]
            },
            {
                "id": "ml",
                "content": "Machine learning expertise using scikit-learn and TensorFlow for data science",
                "keywords": ["machine", "learning", "ml", "ai", "tensorflow", "scikit", "data", "science"]
            },
            {
                "id": "data_analysis",
                "content": "Data analysis with pandas and numpy for business intelligence and reporting",
                "keywords": ["data", "analysis", "pandas", "numpy", "business", "intelligence", "reporting"]
            },
            {
                "id": "databases",
                "content": "SQL database design and optimization for large datasets and performance tuning",
                "keywords": ["sql", "database", "optimization", "performance", "datasets"]
            },
            {
                "id": "frontend",
                "content": "React.js frontend development with modern JavaScript and responsive design",
                "keywords": ["react", "frontend", "javascript", "ui", "responsive", "design"]
            },
            {
                "id": "apis",
                "content": "RESTful API development using FastAPI and Django for microservices",
                "keywords": ["api", "rest", "fastapi", "django", "microservices", "backend"]
            },
            {
                "id": "cloud",
                "content": "Cloud deployment experience with AWS, Docker containers and DevOps",
                "keywords": ["cloud", "aws", "docker", "devops", "deployment", "containers"]
            },
            {
                "id": "management",
                "content": "Project management skills with Agile methodologies and team leadership",
                "keywords": ["project", "management", "agile", "leadership", "team", "scrum"]
            }
        ]

    def _score_document(self, doc: Dict[str, str], query_words: List[str]) -> float:
        """Simple keyword matching score"""
        score = 0
        doc_keywords = doc["keywords"]
        doc_content = doc["content"].lower()

        for word in query_words:
            # Exact keyword match
            if word in doc_keywords:
                score += 2
            # Partial content match
            elif word in doc_content:
                score += 1

        return score

    def query(self, question: str, n_results: int = 3) -> str:
        """Query the simple RAG system"""
        try:
            # Extract keywords from question
            query_words = re.findall(r'\b\w+\b', question.lower())

            # Score documents
            scored_docs = []
            for doc in self.documents:
                score = self._score_document(doc, query_words)
                if score > 0:
                    scored_docs.append((score, doc))

            # Sort by score and get top results
            scored_docs.sort(key=lambda x: x[0], reverse=True)
            top_docs = scored_docs[:n_results]

            if not top_docs:
                return "No relevant skills found in the CV for your query."

            # Format results
            skills = [doc["content"] for score, doc in top_docs]
            formatted_skills = "\n".join([f"• {skill}" for skill in skills])

            return f"Current skills found in CV:\n{formatted_skills}"

        except Exception as e:
            return f"RAG query error: {str(e)}"

# Global RAG instance
rag_system = SimpleRAG()

def query_local_rag(question: str, conversation_id: str = None) -> str:
    """Function compatible with the existing MCP interface"""
    return rag_system.query(question)