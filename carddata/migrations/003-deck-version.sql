-- Existing decks remain V1. New application saves explicitly specify V2.
ALTER TABLE decks ADD COLUMN card_data_version TINYINT NOT NULL DEFAULT 1;
