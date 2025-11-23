-- Schema for OCS Cloud Server
-- This file contains the SQL schema for the Supabase database

-- Users table (already exists)
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     userid VARCHAR(255) UNIQUE NOT NULL,
--     passwordhash VARCHAR(255) NOT NULL,
--     role VARCHAR(50) NOT NULL DEFAULT 'user',
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id VARCHAR(255) REFERENCES users(userid),
    repository_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Project members table (for group projects and invitations)
CREATE TABLE IF NOT EXISTS project_members (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    user_id VARCHAR(255) REFERENCES users(userid) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'accepted', 'declined'
    role VARCHAR(50) DEFAULT 'member', -- 'owner', 'admin', 'member'
    invited_by VARCHAR(255) REFERENCES users(userid),
    invited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP,
    UNIQUE(project_id, user_id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_project_members_user_id ON project_members(user_id);
CREATE INDEX IF NOT EXISTS idx_project_members_project_id ON project_members(project_id);
CREATE INDEX IF NOT EXISTS idx_project_members_status ON project_members(status);
CREATE INDEX IF NOT EXISTS idx_projects_owner_id ON projects(owner_id);

-- Sample data for testing
-- Insert sample projects
-- INSERT INTO projects (name, description, owner_id, repository_url) VALUES
-- ('Sample Project 1', 'A sample coding project', 'admin_test', 'https://github.com/sample/project1'),
-- ('Sample Project 2', 'Another sample project', 'admin_test', 'https://github.com/sample/project2');

-- Insert sample invitations
-- INSERT INTO project_members (project_id, user_id, status, role, invited_by) VALUES
-- (1, 'user_test', 'pending', 'member', 'admin_test'),
-- (2, 'user_test', 'accepted', 'member', 'admin_test');
