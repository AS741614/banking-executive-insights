-- ==========================================
-- INSTITUTIONAL GOVERNANCE & COGNITION SCHEMA
-- ==========================================

CREATE SCHEMA IF NOT EXISTS governance;

-- 1. Governance Tiers
CREATE TABLE IF NOT EXISTS governance.tiers (
    tier_id SERIAL PRIMARY KEY,
    tier_name TEXT UNIQUE NOT NULL,
    risk_threshold NUMERIC(4,2),
    approval_requirement TEXT
);

-- 2. Policy Drift Matrix
CREATE TABLE IF NOT EXISTS governance.policy_drift (
    drift_id SERIAL PRIMARY KEY,
    policy_domain TEXT NOT NULL,
    alignment_score NUMERIC(5,2),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'ACTIVE'
);

-- 3. Cognition Event Persistence
CREATE TABLE IF NOT EXISTS governance.cognition_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    domain TEXT NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB
);

-- 4. Audit Runtime Logs
CREATE TABLE IF NOT EXISTS governance.audit_logs (
    audit_id SERIAL PRIMARY KEY,
    trace_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Initial Governance Seed
INSERT INTO governance.tiers (tier_name, risk_threshold, approval_requirement)
VALUES 
('TIER_1_STANDARD', 0.10, 'AUTOMATED'),
('TIER_2_ENHANCED', 0.25, 'SUPERVISOR'),
('TIER_3_RESTRICTED', 0.50, 'COMPLIANCE_OFFICER'),
('TIER_4_INSTITUTIONAL', 0.85, 'BOARD_DIRECTORS')
ON CONFLICT (tier_name) DO NOTHING;

-- Initial Drift Targets
INSERT INTO governance.policy_drift (policy_domain, alignment_score, status)
VALUES 
('AML_SURVEILLANCE', 98.2, 'OPTIMAL'),
('KYC_INTELLIGENCE', 99.1, 'OPTIMAL'),
('TREASURY_LIQUIDITY', 82.4, 'DRIFT'),
('FRAUD_PATTERNS', 94.8, 'DEGRADED')
ON CONFLICT DO NOTHING;
