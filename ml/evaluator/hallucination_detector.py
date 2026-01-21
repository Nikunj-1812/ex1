"""
Hallucination Detector
======================

Detects potential hallucinations in AI responses using multiple signals.

Research Component:
- Confidence calibration analysis
- Self-consistency checking
- Uncertainty quantification
- Factual grounding assessment

Author: MAI-PAEP Team
"""

import logging
import re
from typing import Dict, Any, List
import numpy as np

logger = logging.getLogger(__name__)


class HallucinationDetector:
    """
    Detects potential hallucinations in AI-generated text.
    
    Methodology:
    -----------
    Hallucinations occur when AI models generate content that sounds plausible
    but is factually incorrect or unsupported. We use multiple signals:
    
    1. **Confidence Markers**: Detect hedging language ("might", "possibly", "I think")
    2. **Specificity Analysis**: Overly specific claims without sources are risky
    3. **Consistency**: Check for self-contradictions
    4. **Source Attribution**: Lack of sources increases hallucination risk
    5. **Uncertainty Quantification**: Measure epistemic uncertainty
    
    Risk Score Calculation:
    ----------------------
    risk = w1×confidence_risk + w2×specificity_risk + w3×consistency_risk + w4×source_risk
    
    Where weights sum to 1.0 and are tuned based on research findings.
    """
    
    # Weights for different risk factors
    WEIGHTS = {
        "confidence": 0.25,
        "specificity": 0.20,
        "consistency": 0.30,
        "source": 0.25
    }
    
    # Pattern for detecting hedging language (indicates uncertainty)
    HEDGING_PATTERNS = [
        r"\b(might|may|could|possibly|perhaps|maybe|likely|probably)\b",
        r"\b(i think|i believe|in my opinion|it seems|it appears)\b",
        r"\b(generally|typically|usually|often|sometimes)\b"
    ]
    
    # Patterns for strong claims (potential hallucinations if unsourced)
    STRONG_CLAIM_PATTERNS = [
        r"\b(definitely|certainly|always|never|must|guaranteed)\b",
        r"\b(\d{1,2}%|\d+\.\d+%)\b",  # Specific percentages
        r"\b(in \d{4}|on [A-Z][a-z]+ \d{1,2})\b",  # Specific dates
        r"\b(\$[\d,]+|\d+ dollars)\b"  # Specific amounts
    ]
    
    # Patterns for source attribution
    SOURCE_PATTERNS = [
        r"\b(according to|based on|research shows|studies indicate)\b",
        r"\b(source:|reference:|citation:)\b",
        r"\b(published in|reported by|stated by)\b"
    ]
    
    def analyze_hallucination_risk(
        self,
        response: str,
        prompt: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze hallucination risk in a response.
        
        Args:
            response: AI response text to analyze
            prompt: Original prompt (optional, for context)
            
        Returns:
            Dictionary containing:
            - hallucination_risk: 0-100 risk score
            - confidence_analysis: Confidence marker metrics
            - specificity_analysis: Specificity metrics
            - consistency_analysis: Self-consistency metrics
            - source_analysis: Source attribution metrics
            - warnings: List of specific warnings
            - recommendations: Mitigation recommendations
        """
        try:
            # Analyze different risk factors
            confidence_score = self._analyze_confidence(response)
            specificity_score = self._analyze_specificity(response)
            consistency_score = self._analyze_consistency(response)
            source_score = self._analyze_sources(response)
            
            # Calculate weighted risk score
            hallucination_risk = (
                self.WEIGHTS["confidence"] * confidence_score +
                self.WEIGHTS["specificity"] * specificity_score +
                self.WEIGHTS["consistency"] * consistency_score +
                self.WEIGHTS["source"] * source_score
            )
            
            # Generate warnings
            warnings = self._generate_warnings(
                hallucination_risk,
                confidence_score,
                specificity_score,
                consistency_score,
                source_score
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                hallucination_risk,
                warnings
            )
            
            # Classify risk level
            if hallucination_risk >= 70:
                risk_level = "high"
            elif hallucination_risk >= 40:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "hallucination_risk": round(hallucination_risk, 2),
                "risk_level": risk_level,
                "confidence_analysis": {
                    "score": round(confidence_score, 2),
                    "hedging_count": self._count_patterns(response, self.HEDGING_PATTERNS)
                },
                "specificity_analysis": {
                    "score": round(specificity_score, 2),
                    "strong_claim_count": self._count_patterns(response, self.STRONG_CLAIM_PATTERNS)
                },
                "consistency_analysis": {
                    "score": round(consistency_score, 2)
                },
                "source_analysis": {
                    "score": round(source_score, 2),
                    "source_count": self._count_patterns(response, self.SOURCE_PATTERNS)
                },
                "warnings": warnings,
                "recommendations": recommendations,
                "method": "multi-signal"
            }
            
        except Exception as e:
            logger.error(f"Hallucination analysis failed: {e}")
            return self._default_analysis()
    
    def _analyze_confidence(self, text: str) -> float:
        """
        Analyze confidence markers in text.
        
        Low confidence language → Lower risk (AI is uncertain)
        High confidence without sources → Higher risk (overconfident)
        
        Returns:
            Risk score 0-100
        """
        hedging_count = self._count_patterns(text, self.HEDGING_PATTERNS)
        word_count = len(text.split())
        
        if word_count == 0:
            return 50.0
        
        # Calculate hedging ratio
        hedging_ratio = hedging_count / (word_count / 100)  # per 100 words
        
        # More hedging = less risk (AI is appropriately uncertain)
        # Less hedging = more risk (AI might be overconfident)
        if hedging_ratio >= 3.0:
            return 20.0  # Low risk - appropriate uncertainty
        elif hedging_ratio >= 1.5:
            return 40.0  # Medium-low risk
        elif hedging_ratio >= 0.5:
            return 60.0  # Medium-high risk
        else:
            return 80.0  # High risk - overly confident
    
    def _analyze_specificity(self, text: str) -> float:
        """
        Analyze specificity of claims.
        
        Overly specific claims (exact numbers, dates, percentages)
        without sources are hallucination red flags.
        
        Returns:
            Risk score 0-100
        """
        strong_claim_count = self._count_patterns(text, self.STRONG_CLAIM_PATTERNS)
        source_count = self._count_patterns(text, self.SOURCE_PATTERNS)
        
        if strong_claim_count == 0:
            return 30.0  # No strong claims, low risk
        
        # Calculate specificity ratio
        # High specificity + low sources = high risk
        if source_count >= strong_claim_count:
            return 25.0  # Claims are sourced
        elif source_count >= strong_claim_count * 0.5:
            return 45.0  # Some sourcing
        else:
            # High specificity without sources
            risk = min(90.0, 50.0 + (strong_claim_count * 10))
            return risk
    
    def _analyze_consistency(self, text: str) -> float:
        """
        Analyze internal consistency.
        
        Self-contradictions are strong hallucination indicators.
        
        Returns:
            Risk score 0-100
        """
        # Split into sentences
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        
        if len(sentences) < 2:
            return 30.0  # Too short to check consistency
        
        # Look for contradiction markers
        contradiction_patterns = [
            r"\b(however|but|although|yet|contrary to|on the other hand)\b"
        ]
        
        contradiction_count = self._count_patterns(text, contradiction_patterns)
        
        # Some contradictions are normal (nuanced discussion)
        # Too many suggest confusion or hallucination
        if contradiction_count == 0:
            return 35.0  # No contradictions found
        elif contradiction_count <= 2:
            return 45.0  # Normal level of nuance
        else:
            return min(85.0, 50.0 + (contradiction_count * 15))
    
    def _analyze_sources(self, text: str) -> float:
        """
        Analyze source attribution.
        
        Lack of sources for factual claims increases hallucination risk.
        
        Returns:
            Risk score 0-100
        """
        source_count = self._count_patterns(text, self.SOURCE_PATTERNS)
        word_count = len(text.split())
        
        if word_count < 50:
            return 40.0  # Short response, sources less critical
        
        # Calculate source density (sources per 100 words)
        source_density = (source_count / word_count) * 100
        
        if source_density >= 2.0:
            return 20.0  # Well-sourced
        elif source_density >= 1.0:
            return 35.0  # Moderately sourced
        elif source_density >= 0.5:
            return 55.0  # Lightly sourced
        else:
            return 75.0  # Poorly sourced
    
    def _count_patterns(self, text: str, patterns: List[str]) -> int:
        """Count occurrences of regex patterns in text."""
        count = 0
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            count += len(matches)
        
        return count
    
    def _generate_warnings(
        self,
        overall_risk: float,
        confidence_score: float,
        specificity_score: float,
        consistency_score: float,
        source_score: float
    ) -> List[str]:
        """Generate specific warnings based on risk scores."""
        warnings = []
        
        if overall_risk >= 60:
            warnings.append("High hallucination risk detected")
        
        if confidence_score >= 70:
            warnings.append("Response shows overconfidence without appropriate hedging")
        
        if specificity_score >= 70:
            warnings.append("Contains specific claims that lack source attribution")
        
        if consistency_score >= 70:
            warnings.append("Potential internal inconsistencies detected")
        
        if source_score >= 70:
            warnings.append("Insufficient source attribution for factual claims")
        
        return warnings
    
    def _generate_recommendations(
        self,
        risk: float,
        warnings: List[str]
    ) -> List[str]:
        """Generate recommendations based on risk level."""
        recommendations = []
        
        if risk >= 60:
            recommendations.append("Verify facts with authoritative sources")
            recommendations.append("Cross-check claims with multiple AI models")
            recommendations.append("Consult domain experts for critical decisions")
        elif risk >= 40:
            recommendations.append("Consider verifying key claims")
            recommendations.append("Use this response as a starting point, not final answer")
        else:
            recommendations.append("Response appears reliable, but always verify critical information")
        
        return recommendations
    
    def _default_analysis(self) -> Dict[str, Any]:
        """Return default analysis when detection fails."""
        return {
            "hallucination_risk": 50.0,
            "risk_level": "medium",
            "confidence_analysis": {"score": 50.0},
            "specificity_analysis": {"score": 50.0},
            "consistency_analysis": {"score": 50.0},
            "source_analysis": {"score": 50.0},
            "warnings": ["Analysis unavailable"],
            "recommendations": ["Verify important claims"],
            "method": "default"
        }
