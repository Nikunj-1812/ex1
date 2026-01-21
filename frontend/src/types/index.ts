/**
 * Type Definitions for MAI-PAEP Frontend
 * Contains all TypeScript interfaces and types
 */

export enum AIModel {
  GPT_4 = 'gpt-4',
  GPT_35_TURBO = 'gpt-3.5-turbo',
  CLAUDE_3_OPUS = 'claude-3-opus',
  CLAUDE_3_SONNET = 'claude-3-sonnet',
  GEMINI_PRO = 'gemini-pro',
  LLAMA_3_70B = 'llama-3-70b',
  MISTRAL_LARGE = 'mistral-large',
}

export enum Domain {
  GENERAL = 'general',
  TECHNICAL = 'technical',
  MEDICAL = 'medical',
  LEGAL = 'legal',
  CREATIVE = 'creative',
  BUSINESS = 'business',
  ACADEMIC = 'academic',
}

export enum SafetyLevel {
  SAFE = 'safe',
  CAUTION = 'caution',
  WARNING = 'warning',
  CRITICAL = 'critical',
}

export interface AIModelInfo {
  id: AIModel;
  name: string;
  provider: string;
  icon: string;
  color: string;
  description: string;
  strengths: string[];
}

export interface EvaluationScores {
  accuracy: number;
  relevance: number;
  clarity: number;
  hallucination_risk: number;
  trust_score: number;
  coherence?: number;
  specificity?: number;
}

export interface AIResponseData {
  model: AIModel;
  response_text: string;
  response_time: number;
  token_count: number;
  cost: number;
  error?: string;
  evaluation_scores: EvaluationScores;
  ranking: number;
  is_best: boolean;
}

export interface DomainClassification {
  domain: Domain;
  confidence: number;
  safety_level: SafetyLevel;
  warnings: string[];
}

export interface PromptSubmitRequest {
  prompt_text: string;
  selected_models: AIModel[];
  user_id?: string;
}

export interface PromptSubmitResponse {
  session_id: string;
  prompt_text: string;
  timestamp: string;
  domain_classification: DomainClassification;
  ai_responses: AIResponseData[];
  best_model: AIModel;
  total_cost: number;
  processing_time: number;
}

export interface ChartDataPoint {
  name: string;
  value: number;
  color?: string;
}

export interface RadarChartData {
  model: string;
  accuracy: number;
  relevance: number;
  clarity: number;
  trust: number;
}

export interface SessionHistory {
  session_id: string;
  prompt_text: string;
  timestamp: string;
  best_model: AIModel;
  models_count: number;
}

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export interface LoadingState {
  isLoading: boolean;
  message: string;
  progress?: number;
}
