-- Initialize the inventory database
CREATE DATABASE inventory_db;

-- Create a user for the application
CREATE USER inventory_user WITH PASSWORD 'inventory_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;

-- Connect to the inventory database
\c inventory_db;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO inventory_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO inventory_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO inventory_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO inventory_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO inventory_user;
