-- Utworzenie bazy danych (jeśli nie została utworzona przez Terraform)
CREATE DATABASE usersdb;

-- Przełącz się na bazę usersdb
\c usersdb;

-- Utworzenie tabeli users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Dodanie użytkownika admin z hasłem admin
INSERT INTO users (username, password) VALUES ('admin', 'admin');
