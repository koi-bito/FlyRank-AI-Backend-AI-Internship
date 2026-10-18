-- Database Initialization Script for Postgres in Docker
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed initial tasks if table is empty
INSERT INTO tasks (title, done)
SELECT title, done FROM (VALUES 
    ('Review FL-01 workflow audit', TRUE),
    ('Build BE-01 CRUD API with FastAPI', TRUE),
    ('Containerize Postgres Stack for BE-04', FALSE)
) AS seed(title, done)
WHERE NOT EXISTS (SELECT 1 FROM tasks LIMIT 1);
