-- Run once before applying SQL from gen-sql.py. Existing IDs are unchanged.
ALTER TABLE cards
    ADD COLUMN source_app_card_id BIGINT NULL,
    ADD COLUMN source_app_management_number VARCHAR(100) NULL,
    ADD COLUMN source_app_detail JSON NULL,
    ADD COLUMN battle_power_4 INT NULL;

-- TiDB resolves indexed columns after the column-add DDL completes.
ALTER TABLE cards
    ADD UNIQUE KEY uq_cards_source_app_card_id (source_app_card_id);
