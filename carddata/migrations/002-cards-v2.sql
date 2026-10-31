-- Artwork identity comes exclusively from the official API id.
-- Raw fields preserve boost cards, QUAD BP and nonnumeric codes.
CREATE TABLE IF NOT EXISTS cards_v2 (
  id BIGINT PRIMARY KEY,
  management_number VARCHAR(100) NOT NULL,
  code VARCHAR(100) NOT NULL,
  name VARCHAR(255) NOT NULL,
  listing JSON NOT NULL,
  detail JSON NOT NULL
);
