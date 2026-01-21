"""
Domain Classifier
=================

Classifies prompts into domains and assesses safety levels.

Author: MAI-PAEP Team
"""

import logging
import re
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class DomainClassifier:
    """
    Classifies prompts into domains and assesses safety.
    
    Domains:
    - Medical
    - Legal
    - Coding
    - Education
    - Business
    - Mental Health
    - General
    """
    
    # Keywords for each domain
    DOMAIN_KEYWORDS = {
        "medical": [
            "symptom", "disease", "doctor", "medicine", "treatment", "diagnosis",
            "health", "illness", "pain", "infection", "prescription", "surgery",
            "hospital", "clinic", "drug", "medication", "fever", "cancer", "diabetes"
        ],
        "legal": [
            "law", "legal", "court", "lawyer", "attorney", "contract", "lawsuit",
            "rights", "lawsuit", "judge", "criminal", "civil", "statute", "regulation",
            "compliance", "liable", "liability", "plaintiff", "defendant"
        ],
        "coding": [
            "code", "programming", "function", "variable", "bug", "debug", "algorithm",
            "python", "javascript", "java", "api", "database", "software", "developer",
            "compile", "syntax", "error", "class", "method", "array"
        ],
        "education": [
            "learn", "study", "student", "teacher", "school", "university", "course",
            "lesson", "homework", "exam", "test", "grade", "education", "tutorial",
            "explain", "understand", "concept", "theory"
        ],
        "business": [
            "business", "company", "market", "sales", "profit", "revenue", "strategy",
            "management", "customer", "product", "service", "invest", "finance",
            "entrepreneur", "startup", "marketing", "brand"
        ],
        "mental_health": [
            "anxiety", "depression", "stress", "therapy", "counseling", "mental",
            "emotion", "feeling", "suicide", "self-harm", "trauma", "ptsd",
            "psychological", "psychiatrist", "mood", "panic"
        ]
    }
    
    # Sensitive patterns that require warnings
    SENSITIVE_PATTERNS = {
        "medical_emergency": [
            r"\b(emergency|urgent|severe pain|chest pain|cant breathe)\b",
            r"\b(overdose|poisoning|bleeding heavily)\b"
        ],
        "mental_health_crisis": [
            r"\b(suicide|kill myself|end my life|want to die)\b",
            r"\b(self-harm|cutting myself|hurt myself)\b"
        ],
        "legal_liability": [
            r"\b(sue|lawsuit|legal action|court case)\b"
        ]
    }
    
    def classify(self, prompt: str) -> Dict[str, Any]:
        """
        Classify prompt and assess safety.
        
        Args:
            prompt: User's prompt text
            
        Returns:
            Classification result with domain, confidence, and safety info
        """
        try:
            prompt_lower = prompt.lower()
            
            # Score each domain
            domain_scores = {}
            for domain, keywords in self.DOMAIN_KEYWORDS.items():
                score = sum(1 for kw in keywords if kw in prompt_lower)
                domain_scores[domain] = score
            
            # Determine primary domain
            if max(domain_scores.values()) == 0:
                domain = "general"
                confidence = 1.0
            else:
                domain = max(domain_scores, key=domain_scores.get)
                # Normalize confidence
                total_matches = sum(domain_scores.values())
                confidence = domain_scores[domain] / total_matches if total_matches > 0 else 0.5
            
            # Check for sensitive content
            is_sensitive, sensitive_type = self._check_sensitive(prompt_lower)
            
            # Determine safety level
            safety_level = self._determine_safety_level(domain, is_sensitive, sensitive_type)
            
            # Generate warnings and recommendations
            warnings = self._generate_warnings(domain, is_sensitive, sensitive_type)
            recommendations = self._generate_recommendations(domain, safety_level)
            
            return {
                "domain": domain,
                "confidence": round(confidence, 3),
                "is_sensitive": is_sensitive,
                "sensitive_type": sensitive_type,
                "safety_level": safety_level,
                "warnings": warnings,
                "recommendations": recommendations,
                "all_scores": domain_scores
            }
            
        except Exception as e:
            logger.error(f"Domain classification failed: {e}")
            return self._default_classification()
    
    def _check_sensitive(self, text: str) -> Tuple[bool, str]:
        """Check for sensitive content."""
        for sensitive_type, patterns in self.SENSITIVE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return True, sensitive_type
        
        return False, None
    
    def _determine_safety_level(
        self,
        domain: str,
        is_sensitive: bool,
        sensitive_type: str
    ) -> str:
        """Determine safety level."""
        if is_sensitive:
            if sensitive_type in ["medical_emergency", "mental_health_crisis"]:
                return "critical"
            else:
                return "warning"
        
        if domain in ["medical", "legal", "mental_health"]:
            return "warning"
        
        return "safe"
    
    def _generate_warnings(
        self,
        domain: str,
        is_sensitive: bool,
        sensitive_type: str
    ) -> List[str]:
        """Generate appropriate warnings."""
        warnings = []
        
        if sensitive_type == "medical_emergency":
            warnings.append("⚠️ MEDICAL EMERGENCY: Call emergency services immediately")
            warnings.append("Do not rely on AI for emergency medical situations")
        
        elif sensitive_type == "mental_health_crisis":
            warnings.append("⚠️ CRISIS DETECTED: Contact crisis hotline immediately")
            warnings.append("National Suicide Prevention Lifeline: 988")
            warnings.append("AI cannot provide crisis intervention")
        
        elif domain == "medical":
            warnings.append("Medical information should be verified with healthcare professionals")
            warnings.append("AI cannot diagnose or prescribe treatment")
        
        elif domain == "legal":
            warnings.append("Legal information is not legal advice")
            warnings.append("Consult a licensed attorney for legal matters")
        
        elif domain == "mental_health":
            warnings.append("AI cannot replace professional mental health care")
            warnings.append("Seek help from licensed mental health professionals")
        
        return warnings
    
    def _generate_recommendations(
        self,
        domain: str,
        safety_level: str
    ) -> List[str]:
        """Generate recommendations based on domain and safety."""
        recommendations = []
        
        if safety_level == "critical":
            recommendations.append("Seek immediate professional help")
            recommendations.append("Do not delay - contact emergency services")
        
        elif safety_level == "warning":
            if domain == "medical":
                recommendations.append("Consult with a doctor or healthcare provider")
                recommendations.append("Use AI response as general information only")
            
            elif domain == "legal":
                recommendations.append("Consult with a licensed attorney")
                recommendations.append("Legal situations vary by jurisdiction")
            
            elif domain == "mental_health":
                recommendations.append("Speak with a licensed therapist or counselor")
                recommendations.append("Use crisis hotlines if in immediate distress")
        
        else:
            recommendations.append("AI responses are helpful but may contain errors")
            recommendations.append("Verify important information from reliable sources")
        
        return recommendations
    
    def _default_classification(self) -> Dict[str, Any]:
        """Return default classification."""
        return {
            "domain": "general",
            "confidence": 0.5,
            "is_sensitive": False,
            "sensitive_type": None,
            "safety_level": "safe",
            "warnings": [],
            "recommendations": ["Verify important information"],
            "all_scores": {}
        }
