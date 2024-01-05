CREATE TABLE IF NOT EXISTS country (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(3) NOT NULL
);

CREATE INDEX idx_country_code ON country (code);

INSERT INTO country (name, code) VALUES
    ('United States', 'US'),
    ('Canada', 'CA'),
    ('United Kingdom', 'GB'),
    ('Germany', 'DE'),
    ('France', 'FR');
