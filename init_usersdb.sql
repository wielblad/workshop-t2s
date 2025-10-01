-- Utworzenie tabeli users jeśli nie istnieje
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Dodanie użytkownika admin
INSERT INTO users (username, password) VALUES ('admin', 'admin') ON CONFLICT (username) DO NOTHING;
