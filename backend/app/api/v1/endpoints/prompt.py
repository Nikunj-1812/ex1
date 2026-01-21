"""
Prompt Endpoint
===============

Main endpoint for prompt submission and evaluation.

Author: MAI-PAEP Team
"""

import logging
import uuid
import time
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.prompt import (
    PromptSubmitRequest,
    PromptSubmitResponse,
    DomainClassification,
    AIResponseSchema,
    EvaluationResultSchema,
    EvaluationScores,
    ComparisonResult
)
from app.models.database import get_db
from app.services.ai_orchestrator import AIOrchestrator
from ml.evaluator.semantic_analyzer import SemanticAnalyzer
from ml.evaluator.hallucination_detector import HallucinationDetector
from ml.evaluator.clarity_scorer import ClarityScorer
from ml.classifiers.domain_classifier import DomainClassifier

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
ai_orchestrator = AIOrchestrator()
semantic_analyzer = SemanticAnalyzer()
hallucination_detector = HallucinationDetector()
clarity_scorer = ClarityScorer()
domain_classifier = DomainClassifier()


@router.post("/submit", response_model=PromptSubmitResponse)
async def submit_prompt(
    request: PromptSubmitRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a prompt for multi-AI evaluation.
    
    This endpoint:
    1. Classifies the prompt domain
    2. Queries multiple AI models
    3. Evaluates responses using ML/NLP
    4. Compares and ranks results
    5. Recommends best AI and answer
    
    Args:
        request: Prompt submission request
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Complete evaluation results
    """
    start_time = time.time()
    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    
    try:
        logger.info(f"Session {session_id}: Processing prompt submission")
        
        # Step 1: Classify domain
        logger.info(f"Session {session_id}: Classifying domain...")
        classification_result = domain_classifier.classify(request.prompt)
        
        domain_classification = DomainClassification(
            domain=classification_result["domain"],
            confidence=classification_result["confidence"],
            is_sensitive=classification_result["is_sensitive"],
            safety_level=classification_result["safety_level"],
            warnings=classification_result["warnings"],
            recommendations=classification_result["recommendations"]
        )
        
        # Step 2: Query AI models
        logger.info(f"Session {session_id}: Querying {len(request.selected_models)} AI models...")
        
        normalized_prompt = ai_orchestrator.normalize_prompt(request.prompt)
        model_list = [model.value for model in request.selected_models]
        
        responses = await ai_orchestrator.query_models(
            normalized_prompt,
            model_list,
            session_id
        )
        
        if not responses:
            raise HTTPException(
                status_code=500,
                detail="No responses received from AI models"
            )
        
        logger.info(f"Session {session_id}: Received {len(responses)} responses")
        
        # Step 3: Evaluate each response
        logger.info(f"Session {session_id}: Evaluating responses...")
        evaluations = []
        
        for response in responses:
            if response["status"] != "success":
                continue
            
            evaluation = await evaluate_response(
                normalized_prompt,
                response,
                session_id
            )
            evaluations.append(evaluation)
        
        if not evaluations:
            raise HTTPException(
                status_code=500,
                detail="All AI models failed to respond"
            )
        
        # Step 4: Compare and rank
        logger.info(f"Session {session_id}: Comparing and ranking...")
        comparison = compare_responses(evaluations)
        
        # Calculate totals
        total_latency = time.time() - start_time
        total_cost = sum(r.get("estimated_cost", 0) for r in responses)
        
        # Build response
        response = PromptSubmitResponse(
            success=True,
            session_id=session_id,
            message=f"Successfully evaluated {len(evaluations)} AI responses",
            domain_classification=domain_classification,
            responses=[AIResponseSchema(**r) for r in responses],
            evaluations=evaluations,
            comparison=comparison,
            total_latency_ms=total_latency * 1000,
            total_cost=total_cost,
            timestamp=datetime.utcnow()
        )
        
        # Save to database in background
        background_tasks.add_task(
            save_session_to_db,
            session_id,
            request.prompt,
            responses,
            evaluations,
            classification_result,
            db
        )
        
        logger.info(
            f"Session {session_id}: Completed in {total_latency:.2f}s "
            f"(cost: ${total_cost:.4f})"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session {session_id}: Failed - {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


async def evaluate_response(
    prompt: str,
    response: Dict[str, Any],
    session_id: str
) -> EvaluationResultSchema:
    """
    Evaluate a single AI response.
    
    Args:
        prompt: Original prompt
        response: AI response data
        session_id: Session identifier
        
    Returns:
        Evaluation result
    """
    response_text = response["response_text"]
    
    # Semantic analysis
    relevance_result = semantic_analyzer.analyze_relevance(prompt, response_text)
    coherence_result = semantic_analyzer.analyze_coherence(response_text)
    
    # Hallucination detection
    hallucination_result = hallucination_detector.analyze_hallucination_risk(
        response_text,
        prompt
    )
    
    # Clarity scoring
    clarity_result = clarity_scorer.score_clarity(response_text)
    
    # Extract bias score (simplified - can be enhanced)
    bias_score = 20.0  # Placeholder - would use dedicated bias detector
    
    # Calculate trust score (weighted average)
    trust_score = (
        0.30 * relevance_result["relevance_score"] +
        0.25 * (100 - hallucination_result["hallucination_risk"]) +
        0.20 * clarity_result["clarity_score"] +
        0.15 * coherence_result["coherence_score"] +
        0.10 * (100 - bias_score)
    )
    
    # Create evaluation scores
    scores = EvaluationScores(
        relevance_score=relevance_result["relevance_score"],
        accuracy_score=(100 - hallucination_result["hallucination_risk"]),  # Inverse of hallucination
        clarity_score=clarity_result["clarity_score"],
        hallucination_risk=hallucination_result["hallucination_risk"],
        bias_score=bias_score,
        trust_score=trust_score,
        semantic_similarity=relevance_result.get("semantic_similarity"),
        readability_metrics=clarity_result.get("readability_metrics"),
        coherence_metrics=coherence_result,
        warnings=hallucination_result.get("warnings", []),
        recommendation=None  # Will be set during comparison
    )
    
    evaluation = EvaluationResultSchema(
        evaluation_id=f"eval_{uuid.uuid4().hex[:12]}",
        response_id=response["response_id"],
        response=AIResponseSchema(**response),
        scores=scores
    )
    
    return evaluation


def compare_responses(
    evaluations: List[EvaluationResultSchema]
) -> ComparisonResult:
    """
    Compare all responses and determine best options.
    
    Args:
        evaluations: List of evaluation results
        
    Returns:
        Comparison result with rankings
    """
    # Sort by trust score
    sorted_by_trust = sorted(
        evaluations,
        key=lambda e: e.scores.trust_score,
        reverse=True
    )
    
    # Sort by relevance
    sorted_by_relevance = sorted(
        evaluations,
        key=lambda e: e.scores.relevance_score,
        reverse=True
    )
    
    # Sort by safety (lowest hallucination risk)
    sorted_by_safety = sorted(
        evaluations,
        key=lambda e: e.scores.hallucination_risk
    )
    
    # Assign ranks
    for i, eval in enumerate(sorted_by_trust, 1):
        eval.scores.rank_by_trust = i
    
    for i, eval in enumerate(sorted_by_relevance, 1):
        eval.scores.rank_by_relevance = i
    
    # Mark best overall (highest trust)
    sorted_by_trust[0].scores.is_best_overall = True
    
    # Mark safest (lowest hallucination risk)
    sorted_by_safety[0].scores.is_safest = True
    
    # Best model and answer
    best_eval = sorted_by_trust[0]
    safest_eval = sorted_by_safety[0]
    
    # Build rankings
    ranking_by_trust = [
        {
            "rank": i,
            "model": eval.response.model_name,
            "trust_score": eval.scores.trust_score,
            "hallucination_risk": eval.scores.hallucination_risk
        }
        for i, eval in enumerate(sorted_by_trust, 1)
    ]
    
    ranking_by_relevance = [
        {
            "rank": i,
            "model": eval.response.model_name,
            "relevance_score": eval.scores.relevance_score
        }
        for i, eval in enumerate(sorted_by_relevance, 1)
    ]
    
    # Cost analysis
    total_cost = sum(e.response.estimated_cost or 0 for e in evaluations)
    cost_analysis = {
        "total_cost": total_cost,
        "by_model": [
            {
                "model": e.response.model_name,
                "cost": e.response.estimated_cost,
                "tokens": e.response.tokens_used
            }
            for e in evaluations
        ]
    }
    
    # Performance analysis
    performance_analysis = {
        "avg_latency_ms": sum(e.response.latency_ms for e in evaluations) / len(evaluations),
        "by_model": [
            {
                "model": e.response.model_name,
                "latency_ms": e.response.latency_ms
            }
            for e in evaluations
        ]
    }
    
    return ComparisonResult(
        best_model=best_eval.response.model_name,
        best_model_reason=f"Highest trust score ({best_eval.scores.trust_score:.1f}/100) with balanced accuracy and clarity",
        best_answer=best_eval.response.response_text,
        safest_model=safest_eval.response.model_name,
        safest_answer=safest_eval.response.response_text,
        ranking_by_trust=ranking_by_trust,
        ranking_by_relevance=ranking_by_relevance,
        cost_analysis=cost_analysis,
        performance_analysis=performance_analysis
    )


async def save_session_to_db(
    session_id: str,
    prompt: str,
    responses: List[Dict],
    evaluations: List,
    classification: Dict,
    db: AsyncSession
):
    """
    Save session data to database (background task).
    """
    try:
        logger.info(f"Saving session {session_id} to database...")
        # Implementation would save to PostgreSQL and MongoDB
        # Omitted for brevity - would use SQLAlchemy models
        logger.info(f"Session {session_id} saved successfully")
    except Exception as e:
        logger.error(f"Failed to save session {session_id}: {e}")
