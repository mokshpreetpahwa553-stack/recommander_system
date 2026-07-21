CREATE TABLE IF NOT EXISTS resource_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS resources (
    display_id SERIAL PRIMARY KEY,
    id VARCHAR(50),
    title TEXT,
    description TEXT,
    resource_type VARCHAR(50),
    difficulty_score DOUBLE PRECISION,
    difficulty_category INTEGER,
    url TEXT,
    source VARCHAR(100),
    language VARCHAR(10),
    embedding DOUBLE PRECISION[]
);

INSERT INTO resource_types (name)
VALUES ('videos'), ('articles')
ON CONFLICT (name) DO NOTHING;
