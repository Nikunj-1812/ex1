"""
Clarity Scorer
==============

Evaluates readability and clarity of AI responses.

Research Component:
- Readability metrics (Flesch, Fog Index)
- Sentence structure analysis
- Vocabulary complexity
- Coherence scoring

Author: MAI-PAEP Team
"""

import logging
import re
from typing import Dict, Any
import numpy as np

logger = logging.getLogger(__name__)


class ClarityScorer:
    """
    Scores text clarity using multiple readability metrics.
    
    Metrics Implemented:
    -------------------
    1. **Flesch Reading Ease**: 
       Score = 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
       
    2. **Flesch-Kincaid Grade Level**:
       Grade = 0.39(words/sentences) + 11.8(syllables/words) - 15.59
       
    3. **Average Sentence Length**: Optimal range 15-20 words
    
    4. **Vocabulary Complexity**: Ratio of complex words
    
    5. **Structure Score**: Paragraph organization and formatting
    """
    
    def __init__(self):
        """Initialize clarity scorer."""
        pass
    
    def score_clarity(self, text: str) -> Dict[str, Any]:
        """
        Score overall clarity of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing:
            - clarity_score: 0-100 overall score
            - readability_metrics: Detailed readability data
            - suggestions: Improvement suggestions
        """
        try:
            # Calculate base metrics
            word_count = self._count_words(text)
            sentence_count = self._count_sentences(text)
            syllable_count = self._count_syllables(text)
            complex_word_count = self._count_complex_words(text)
            
            if sentence_count == 0 or word_count == 0:
                return self._default_score()
            
            # Calculate readability metrics
            flesch_score = self._flesch_reading_ease(
                word_count, sentence_count, syllable_count
            )
            
            fk_grade = self._flesch_kincaid_grade(
                word_count, sentence_count, syllable_count
            )
            
            avg_sentence_length = word_count / sentence_count
            complexity_ratio = complex_word_count / word_count
            
            # Score individual components
            readability_subscore = self._score_readability(flesch_score)
            length_subscore = self._score_sentence_length(avg_sentence_length)
            complexity_subscore = self._score_complexity(complexity_ratio)
            structure_subscore = self._score_structure(text)
            
            # Weighted average for clarity score
            clarity_score = (
                0.35 * readability_subscore +
                0.25 * length_subscore +
                0.20 * complexity_subscore +
                0.20 * structure_subscore
            )
            
            # Generate suggestions
            suggestions = self._generate_suggestions(
                flesch_score,
                avg_sentence_length,
                complexity_ratio
            )
            
            # Classify clarity level
            if clarity_score >= 80:
                clarity_level = "excellent"
            elif clarity_score >= 65:
                clarity_level = "good"
            elif clarity_score >= 50:
                clarity_level = "moderate"
            else:
                clarity_level = "poor"
            
            return {
                "clarity_score": round(clarity_score, 2),
                "clarity_level": clarity_level,
                "readability_metrics": {
                    "flesch_reading_ease": round(flesch_score, 2),
                    "flesch_kincaid_grade": round(fk_grade, 2),
                    "avg_sentence_length": round(avg_sentence_length, 2),
                    "complex_word_ratio": round(complexity_ratio, 4),
                    "word_count": word_count,
                    "sentence_count": sentence_count,
                    "syllable_count": syllable_count
                },
                "subscores": {
                    "readability": round(readability_subscore, 2),
                    "sentence_length": round(length_subscore, 2),
                    "vocabulary_complexity": round(complexity_subscore, 2),
                    "structure": round(structure_subscore, 2)
                },
                "suggestions": suggestions,
                "method": "multi-metric"
            }
            
        except Exception as e:
            logger.error(f"Clarity scoring failed: {e}")
            return self._default_score()
    
    def _flesch_reading_ease(
        self,
        words: int,
        sentences: int,
        syllables: int
    ) -> float:
        """
        Calculate Flesch Reading Ease score.
        
        Range: 0-100
        90-100: Very Easy (5th grade)
        60-70: Standard (8th-9th grade)
        0-30: Very Difficult (College graduate)
        """
        if sentences == 0 or words == 0:
            return 50.0
        
        score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        return max(0, min(100, score))
    
    def _flesch_kincaid_grade(
        self,
        words: int,
        sentences: int,
        syllables: int
    ) -> float:
        """
        Calculate Flesch-Kincaid Grade Level.
        
        Returns US school grade level required to understand text.
        """
        if sentences == 0 or words == 0:
            return 10.0
        
        grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        return max(0, grade)
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def _count_sentences(self, text: str) -> int:
        """Count sentences in text."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        return max(1, len(sentences))
    
    def _count_syllables(self, text: str) -> int:
        """
        Estimate syllable count.
        
        Simple algorithm:
        - Count vowel groups
        - Adjust for common patterns
        """
        words = re.findall(r'\b\w+\b', text.lower())
        total_syllables = 0
        
        for word in words:
            syllables = self._count_syllables_word(word)
            total_syllables += syllables
        
        return max(1, total_syllables)
    
    def _count_syllables_word(self, word: str) -> int:
        """Count syllables in a single word."""
        word = word.lower()
        syllables = 0
        vowels = 'aeiouy'
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllables += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllables -= 1
        
        # Every word has at least one syllable
        return max(1, syllables)
    
    def _count_complex_words(self, text: str) -> int:
        """
        Count complex words (3+ syllables).
        """
        words = re.findall(r'\b\w+\b', text.lower())
        complex_count = 0
        
        for word in words:
            if len(word) > 6 and self._count_syllables_word(word) >= 3:
                complex_count += 1
        
        return complex_count
    
    def _score_readability(self, flesch_score: float) -> float:
        """
        Convert Flesch score to 0-100 clarity subscore.
        
        Optimal range: 60-70 (standard reading level)
        """
        if 60 <= flesch_score <= 70:
            return 100.0  # Optimal
        elif 50 <= flesch_score < 60:
            return 90.0
        elif 70 < flesch_score <= 80:
            return 90.0
        elif 40 <= flesch_score < 50:
            return 75.0
        elif 80 < flesch_score <= 90:
            return 80.0
        elif 30 <= flesch_score < 40:
            return 60.0
        else:
            return 50.0
    
    def _score_sentence_length(self, avg_length: float) -> float:
        """
        Score sentence length.
        
        Optimal: 15-20 words per sentence
        """
        if 15 <= avg_length <= 20:
            return 100.0
        elif 12 <= avg_length < 15:
            return 90.0
        elif 20 < avg_length <= 25:
            return 85.0
        elif 10 <= avg_length < 12:
            return 75.0
        elif 25 < avg_length <= 30:
            return 70.0
        else:
            # Too short or too long
            return max(40.0, 100.0 - abs(avg_length - 17.5) * 3)
    
    def _score_complexity(self, complexity_ratio: float) -> float:
        """
        Score vocabulary complexity.
        
        Optimal: 10-20% complex words
        """
        if 0.10 <= complexity_ratio <= 0.20:
            return 100.0
        elif 0.05 <= complexity_ratio < 0.10:
            return 85.0
        elif 0.20 < complexity_ratio <= 0.30:
            return 80.0
        elif complexity_ratio < 0.05:
            return 75.0  # Too simple
        else:
            return max(40.0, 100.0 - (complexity_ratio - 0.20) * 200)
    
    def _score_structure(self, text: str) -> float:
        """
        Score text structure and formatting.
        
        Checks for:
        - Paragraph breaks
        - List formatting
        - Logical organization
        """
        score = 70.0  # Base score
        
        # Check for paragraph breaks
        paragraphs = text.split('\n\n')
        if len(paragraphs) > 1:
            score += 10.0
        
        # Check for lists
        if re.search(r'(^|\n)[•\-*]\s', text) or re.search(r'(^|\n)\d+\.\s', text):
            score += 10.0
        
        # Check for headers/sections
        if re.search(r'(^|\n)#{1,3}\s', text) or re.search(r'(^|\n)[A-Z][^.!?]*:(\n|$)', text):
            score += 10.0
        
        return min(100.0, score)
    
    def _generate_suggestions(
        self,
        flesch_score: float,
        avg_sentence_length: float,
        complexity_ratio: float
    ) -> list:
        """Generate improvement suggestions."""
        suggestions = []
        
        if flesch_score < 50:
            suggestions.append("Text is difficult to read. Consider simplifying language.")
        
        if avg_sentence_length > 25:
            suggestions.append("Sentences are too long. Break into shorter sentences.")
        elif avg_sentence_length < 10:
            suggestions.append("Sentences are too short. Consider combining some.")
        
        if complexity_ratio > 0.30:
            suggestions.append("Vocabulary is too complex. Use simpler words where possible.")
        elif complexity_ratio < 0.05:
            suggestions.append("Vocabulary might be too simple for the topic.")
        
        if not suggestions:
            suggestions.append("Clarity is good. No major improvements needed.")
        
        return suggestions
    
    def _default_score(self) -> Dict[str, Any]:
        """Return default score when analysis fails."""
        return {
            "clarity_score": 70.0,
            "clarity_level": "moderate",
            "readability_metrics": {},
            "subscores": {},
            "suggestions": ["Analysis unavailable"],
            "method": "default"
        }
