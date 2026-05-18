#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import mysql from "mysql2/promise";

const BASE_CARD_NUMBER_PATTERN = /[A-Z]+\d{2}-[A-Z]?\d{3}|PR-\d{3}/g;

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const envPath = path.join(repoRoot, ".env.local");

const parseEnvFile = (raw) => {
  const values = {};

  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }

    const separatorIndex = trimmed.indexOf("=");
    if (separatorIndex === -1) {
      continue;
    }

    const key = trimmed.slice(0, separatorIndex).trim();
    let value = trimmed.slice(separatorIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    values[key] = value;
  }

  return values;
};

const readEnv = () => {
  const fileValues = fs.existsSync(envPath)
    ? parseEnvFile(fs.readFileSync(envPath, "utf8"))
    : {};

  return {
    TIDB_HOST: process.env.TIDB_HOST ?? fileValues.TIDB_HOST,
    TIDB_PORT: process.env.TIDB_PORT ?? fileValues.TIDB_PORT,
    TIDB_USER: process.env.TIDB_USER ?? fileValues.TIDB_USER,
    TIDB_PASSWORD: process.env.TIDB_PASSWORD ?? fileValues.TIDB_PASSWORD,
    TIDB_DATABASE: process.env.TIDB_DATABASE ?? fileValues.TIDB_DATABASE,
    TIDB_SSL_CA: process.env.TIDB_SSL_CA ?? fileValues.TIDB_SSL_CA,
    TIDB_SSL_MODE: process.env.TIDB_SSL_MODE ?? fileValues.TIDB_SSL_MODE,
  };
};

const requiredEnv = (env, key) => {
  if (!env[key]) {
    throw new Error(`Missing required env var: ${key}`);
  }
  return env[key];
};

const extractBaseCardKey = (number) => {
  const rawNumber = (number ?? "").trim();
  if (!rawNumber) {
    return "";
  }

  const matches = rawNumber.match(BASE_CARD_NUMBER_PATTERN);
  if (matches && matches.length > 0) {
    return matches[matches.length - 1];
  }

  return rawNumber;
};

const main = async () => {
  const env = readEnv();
  const sslCaPath = env.TIDB_SSL_CA;
  const ssl = sslCaPath
    ? {
        ca: fs.readFileSync(sslCaPath, "utf8"),
        rejectUnauthorized: env.TIDB_SSL_MODE !== "DISABLED",
      }
    : undefined;

  const connection = await mysql.createConnection({
    host: requiredEnv(env, "TIDB_HOST"),
    port: Number(requiredEnv(env, "TIDB_PORT")),
    user: requiredEnv(env, "TIDB_USER"),
    password: requiredEnv(env, "TIDB_PASSWORD"),
    database: requiredEnv(env, "TIDB_DATABASE"),
    ssl,
    charset: "utf8mb4",
  });

  try {
    const databaseName = requiredEnv(env, "TIDB_DATABASE");
    const [columnRows] = await connection.execute(
      `
        SELECT COUNT(*) AS count
        FROM information_schema.columns
        WHERE table_schema = ?
          AND table_name = 'cards'
          AND column_name = 'base_card_key'
      `,
      [databaseName]
    );
    const columnExists = Number(columnRows[0]?.count ?? 0) > 0;

    if (!columnExists) {
      console.log("Adding cards.base_card_key column");
      await connection.execute(
        "ALTER TABLE cards ADD COLUMN base_card_key VARCHAR(32) NULL AFTER number"
      );
    } else {
      console.log("cards.base_card_key already exists");
    }

    console.log("Backfilling cards.base_card_key");
    const [cards] = await connection.execute(
      "SELECT id, number FROM cards WHERE base_card_key IS NULL OR TRIM(base_card_key) = ''"
    );

    let updatedCount = 0;
    for (const card of cards) {
      const baseCardKey = extractBaseCardKey(card.number);
      await connection.execute(
        "UPDATE cards SET base_card_key = ? WHERE id = ?",
        [baseCardKey, card.id]
      );
      updatedCount += 1;
    }
    console.log(`Updated ${updatedCount} rows`);

    const [indexRows] = await connection.execute("SHOW INDEX FROM cards WHERE Key_name = 'idx_cards_base_card_key'");
    if (Array.isArray(indexRows) && indexRows.length === 0) {
      console.log("Creating idx_cards_base_card_key");
      await connection.execute(
        "CREATE INDEX idx_cards_base_card_key ON cards (base_card_key)"
      );
    } else {
      console.log("idx_cards_base_card_key already exists");
    }

    console.log("Migration complete");
  } finally {
    await connection.end();
  }
};

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
