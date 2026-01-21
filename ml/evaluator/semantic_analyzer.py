"""
Semantic Analyzer
=================

Advanced semantic analysis using Sentence-BERT and transformers.

Research Component:
- Semantic similarity measurement
- Prompt-response relevance scoring
- Context coherence analysis

Author: MAI-PAEP Team
"""

import logging
from typing import Dict, Any, List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch

from app.core.config import settings

logger = logging.getLogger(__name__)


class SemanticAnalyzer:
    """
    Analyzes semantic similarity and relevance using state-of-the-art NLP models.
    
    Core Methodology:
    ----------------
    1. **Embedding Generation**: Use Sentence-BERT to generate dense vector representations
    2. **Similarity Computation**: Calculate cosine similarity between embeddings
    3. **Relevance Scoring**: Measure alignment between prompt intent and response
    4. **Coherence Analysis**: Evaluate internal consistency of response
    
    Mathematical Foundation:
    -----------------------
    Cosine Similarity:
        sim(A, B) = (A · B) / (||A|| × ||B||)
    
    Relevance Score:
        relevance = 100 × sim(embed(prompt), embed(response))
    
    Coherence Score:
        coherence = avg(sim(sent_i, sent_i+1)) for all sentence pairs
    """
    
    def __init__(self):
        """
        Initialize semantic analyzer with pre-trained models.
        """
        try:
            # Load Sentence-BERT model
            self.model = SentenceTransformer(
                settings.SBERT_MODEL,
                device=settings.ML_DEVICE
            )
            
            logger.info(f"Loaded Sentence-BERT model: {settings.SBERT_MODEL}")
            
        except Exception as e:
            logger.error(f"Failed to load semantic model: {e}")
            self.model = None
    
    def analyze_relevance(
        self,
        prompt: str,
        response: str
    ) -> Dict[str, Any]:
        """
        Analyze semantic relevance between prompt and response.
        
        Args:
            prompt: User's prompt text
            response: AI model's response text
            
        Returns:
            Dictionary containing:
            - relevance_score: 0-100 score
            - semantic_similarity: Raw cosine similarity
            - alignment_strength: Categorical assessment
            
        Algorithm:
        ---------
        1. Generate embeddings for prompt and response
        2. Calculate cosine similarity
        3. Normalize to 0-100 scale
        4. Classify alignment strength
        """
        if not self.model:
            return self._default_relevance()
        
        try:
            # Generate embeddings
            prompt_embedding = self.model.encode(
                prompt,
                convert_to_tensor=True,
                show_progress_bar=False
            )
            
            response_embedding = self.model.encode(
                response,
                convert_to_tensor=True,
                show_progress_bar=False
            )
            
            # Calculate cosine similarity
            similarity = util.cos_sim(prompt_embedding, response_embedding)[0][0].item()
            
            # Normalize to 0-100 scale
            # Cosine similarity ranges from [-1, 1], we map [0, 1] to [0, 100]
            relevance_score = max(0, min(100, similarity * 100))
            
            # Classify alignment
            if relevance_score >= 80:
                alignment = "excellent"
            elif relevance_score >= 60:
                alignment = "good"
            elif relevance_score >= 40:
                alignment = "moderate"
            else:
                alignment = "poor"
            
            return {
                "relevance_score": round(relevance_score, 2),
                "semantic_similarity": round(similarity, 4),
                "alignment_strength": alignment,
                "method": "sentence-bert",
                "model": settings.SBERT_MODEL
            }
            
        except Exception as e:
            logger.error(f"Relevance analysis failed: {e}")
            return self._default_relevance()
    
    def analyze_coherence(self, text: str) -> Dict[str, Any]:
        """
        Analyze internal coherence of text.
        
        Measures how well sentences flow together by calculating
        average similarity between consecutive sentences.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with coherence metrics
            
        Algorithm:
        ---------
        1. Split text into sentences
        2. Generate embeddings for each sentence
        3. Calculate similarity between consecutive sentences
        4. Average similarities for overall coherence score
        """
        if not self.model:
            return {"coherence_score": 70.0, "method": "default"}
        
        try:
            # Split into sentences
            sentences = self._split_sentences(text)
            
            if len(sentences) < 2:
                # Single sentence, assume high coherence
                return {
                    "coherence_score": 90.0,
                    "sentence_count": len(sentences),
                    "method": "single-sentence"
                }
            
            # Generate embeddings
            embeddings = self.model.encode(
                sentences,
                convert_to_tensor=True,
                show_progress_bar=False
            )
            
            # Calculate consecutive similarities
            similarities = []
            for i in range(len(embeddings) - 1):
                sim = util.cos_sim(embeddings[i], embeddings[i + 1])[0][0].item()
                similarities.append(sim)
            
            # Average similarity as coherence score
            avg_similarity = np.mean(similarities)
            coherence_score = max(0, min(100, avg_similarity * 100))
            
            # Calculate variance for consistency measure
            variance = np.var(similarities)
            
            return {
                "coherence_score": round(coherence_score, 2),
                "sentence_count": len(sentences),
                "similarity_mean": round(avg_similarity, 4),
                "similarity_variance": round(variance, 4),
                "consistency": "high" if variance < 0.05 else "moderate" if variance < 0.15 else "low",
                "method": "consecutive-similarity"
            }
            
        except Exception as e:
            logger.error(f"Coherence analysis failed: {e}")
            return {"coherence_score": 70.0, "method": "default"}
    
    def analyze_cross_response_similarity(
        self,
        responses: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze similarity across multiple AI responses.
        
        Useful for:
        - Detecting consensus
        - Identifying outliers
        - Measuring response diversity
        
        Args:
            responses: List of response texts
            
        Returns:
            Dictionary with cross-response metrics
        """
        if not self.model or len(responses) < 2:
            return {"consensus_score": 50.0, "diversity_score": 50.0}
        
        try:
            # Generate embeddings for all responses
            embeddings = self.model.encode(
                responses,
                convert_to_tensor=True,
                show_progress_bar=False
            )
            
            # Calculate pairwise similarities
            similarities = []
            n = len(embeddings)
            
            for i in range(n):
                for j in range(i + 1, n):
                    sim = util.cos_sim(embeddings[i], embeddings[j])[0][0].item()
                    similarities.append(sim)
            
            # Consensus: high average similarity = high consensus
            avg_similarity = np.mean(similarities)
            consensus_score = max(0, min(100, avg_similarity * 100))
            
            # Diversity: high variance = high diversity
            variance = np.var(similarities)
            diversity_score = min(100, variance * 1000)  # Scale variance
            
            return {
                "consensus_score": round(consensus_score, 2),
                "diversity_score": round(diversity_score, 2),
                "avg_similarity": round(avg_similarity, 4),
                "similarity_variance": round(variance, 4),
                "response_count": n
            }
            
        except Exception as e:
            logger.error(f"Cross-response analysis failed: {e}")
            return {"consensus_score": 50.0, "diversity_score": 50.0}
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Simple implementation - can be enhanced with spaCy or NLTK.
        """
        # Basic sentence splitting
        sentences = []
        for sent in text.replace('!', '.').replace('?', '.').split('.'):
            sent = sent.strip()
            if len(sent) > 10:  # Minimum sentence length
                sentences.append(sent)
        
        return sentences if sentences else [text]
    
    def _default_relevance(self) -> Dict[str, Any]:
        """Return default relevance scores when model unavailable."""
        return {
            "relevance_score": 70.0,
            "semantic_similarity": 0.7,
            "alignment_strength": "moderate",
            "method": "default",
            "model": "none"
        }
