-- MAI-PAEP Database Initialization
-- PostgreSQL Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE IF NOT EXISTS prompt_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    prompt_text TEXT NOT NULL,
    prompt_length INTEGER,
    domain VARCHAR(100),
    is_sensitive BOOLEAN DEFAULT FALSE,
    safety_level VARCHAR(50),
    selected_models JSONB,
    user_id VARCHAR(255),
    ip_address VARCHAR(50),
    user_agent VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS ai_responses (
    id SERIAL PRIMARY KEY,
    response_id VARCHAR(255) UNIQUE NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    model_provider VARCHAR(50),
    response_text TEXT NOT NULL,
    response_length INTEGER,
    latency_ms DOUBLE PRECISION,
    tokens_used INTEGER,
    estimated_cost DOUBLE PRECISION,
    api_version VARCHAR(50),
    finish_reason VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'success',
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS evaluation_results (
    id SERIAL PRIMARY KEY,
    evaluation_id VARCHAR(255) UNIQUE NOT NULL,
    response_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    relevance_score DOUBLE PRECISION NOT NULL,
    accuracy_score DOUBLE PRECISION NOT NULL,
    clarity_score DOUBLE PRECISION NOT NULL,
    hallucination_risk DOUBLE PRECISION NOT NULL,
    bias_score DOUBLE PRECISION NOT NULL,
    trust_score DOUBLE PRECISION NOT NULL,
    semantic_similarity DOUBLE PRECISION,
    readability_metrics JSONB,
    coherence_metrics JSONB,
    factual_consistency JSONB,
    bias_analysis JSONB,
    rank_by_relevance INTEGER,
    rank_by_trust INTEGER,
    is_best_overall BOOLEAN DEFAULT FALSE,
    is_safest BOOLEAN DEFAULT FALSE,
    recommendation TEXT,
    warnings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_feedback (
    id SERIAL PRIMARY KEY,
    feedback_id VARCHAR(255) UNIQUE NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    response_id VARCHAR(255),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    was_helpful BOOLEAN,
    was_accurate BOOLEAN,
    comment TEXT,
    preferred_model VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cost_tracking (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    total_tokens INTEGER,
    input_cost DOUBLE PRECISION,
    output_cost DOUBLE PRECISION,
    total_cost DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_prompt_sessions_session_id ON prompt_sessions(session_id);
CREATE INDEX idx_prompt_sessions_created_at ON prompt_sessions(created_at);
CREATE INDEX idx_prompt_sessions_domain ON prompt_sessions(domain);

CREATE INDEX idx_ai_responses_response_id ON ai_responses(response_id);
CREATE INDEX idx_ai_responses_session_id ON ai_responses(session_id);
CREATE INDEX idx_ai_responses_model_name ON ai_responses(model_name);

CREATE INDEX idx_evaluation_results_evaluation_id ON evaluation_results(evaluation_id);
CREATE INDEX idx_evaluation_results_response_id ON evaluation_results(response_id);
CREATE INDEX idx_evaluation_results_session_id ON evaluation_results(session_id);
CREATE INDEX idx_evaluation_results_trust_score ON evaluation_results(trust_score);

CREATE INDEX idx_user_feedback_session_id ON user_feedback(session_id);
CREATE INDEX idx_user_feedback_rating ON user_feedback(rating);

CREATE INDEX idx_cost_tracking_session_id ON cost_tracking(session_id);
CREATE INDEX idx_cost_tracking_created_at ON cost_tracking(created_at);

-- Add foreign key constraints
ALTER TABLE ai_responses
    ADD CONSTRAINT fk_ai_responses_session
    FOREIGN KEY (session_id)
    REFERENCES prompt_sessions(session_id)
    ON DELETE CASCADE;

ALTER TABLE evaluation_results
    ADD CONSTRAINT fk_evaluation_results_response
    FOREIGN KEY (response_id)
    REFERENCES ai_responses(response_id)
    ON DELETE CASCADE;

ALTER TABLE evaluation_results
    ADD CONSTRAINT fk_evaluation_results_session
    FOREIGN KEY (session_id)
    REFERENCES prompt_sessions(session_id)
    ON DELETE CASCADE;

ALTER TABLE user_feedback
    ADD CONSTRAINT fk_user_feedback_session
    FOREIGN KEY (session_id)
    REFERENCES prompt_sessions(session_id)
    ON DELETE CASCADE;

ALTER TABLE cost_tracking
    ADD CONSTRAINT fk_cost_tracking_session
    FOREIGN KEY (session_id)
    REFERENCES prompt_sessions(session_id)
    ON DELETE CASCADE;

-- Create views for analytics
CREATE OR REPLACE VIEW v_session_summary AS
SELECT
    ps.session_id,
    ps.prompt_text,
    ps.domain,
    ps.safety_level,
    ps.created_at,
    COUNT(DISTINCT ar.response_id) as response_count,
    AVG(ar.latency_ms) as avg_latency_ms,
    SUM(ar.estimated_cost) as total_cost,
    MAX(er.trust_score) as max_trust_score,
    MIN(er.hallucination_risk) as min_hallucination_risk
FROM
    prompt_sessions ps
    LEFT JOIN ai_responses ar ON ps.session_id = ar.session_id
    LEFT JOIN evaluation_results er ON ps.session_id = er.session_id
GROUP BY
    ps.session_id, ps.prompt_text, ps.domain, ps.safety_level, ps.created_at;

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO maipaep_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO maipaep_user;
