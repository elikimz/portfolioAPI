-- Create certificates table
CREATE TABLE IF NOT EXISTS certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR NOT NULL,
    issuer VARCHAR NOT NULL,
    issue_date TIMESTAMP NULL,
    expiry_date TIMESTAMP NULL,
    credential_id VARCHAR NULL,
    credential_url VARCHAR NULL,
    image_url VARCHAR NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_certificates_user_id ON certificates(user_id);

-- Create index on is_deleted for filtering
CREATE INDEX IF NOT EXISTS idx_certificates_is_deleted ON certificates(is_deleted);

-- Update alembic_version to mark the migration as applied
INSERT INTO alembic_version (version_num) VALUES ('add_certificates_table')
ON CONFLICT DO NOTHING;
