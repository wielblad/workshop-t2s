
-- Ustawienie schemy public
SET search_path TO public;

CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO public.users (username, password) VALUES ('admin', 'admin') ON CONFLICT (username) DO NOTHING;
