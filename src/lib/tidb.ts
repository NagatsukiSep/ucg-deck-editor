import "server-only";

import fs from "node:fs";
import mysql, { ResultSetHeader, type Pool } from "mysql2/promise";

let pool: Pool | undefined;
type TiDBParam = string | number | boolean | null;

const getRequiredEnv = (name: string) => {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return value;
};

const getSslConfig = () => {
  const caPath = process.env.TIDB_SSL_CA;
  if (!caPath) {
    return undefined;
  }

  return {
    ca: fs.readFileSync(caPath, "utf8"),
    rejectUnauthorized: process.env.TIDB_SSL_MODE !== "DISABLED",
  };
};

export const getTiDBPool = () => {
  if (!pool) {
    pool = mysql.createPool({
      host: getRequiredEnv("TIDB_HOST"),
      port: Number(getRequiredEnv("TIDB_PORT")),
      user: getRequiredEnv("TIDB_USER"),
      password: getRequiredEnv("TIDB_PASSWORD"),
      database: getRequiredEnv("TIDB_DATABASE"),
      ssl: getSslConfig(),
      waitForConnections: true,
      connectionLimit: 10,
      charset: "utf8mb4",
    });
  }

  return pool;
};

export const queryTiDB = async <T>(sql: string, params: TiDBParam[] = []) => {
  const [rows] = await getTiDBPool().execute(sql, params);
  return rows as T;
};

export const executeTiDB = async (sql: string, params: TiDBParam[] = []) => {
  const [result] = await getTiDBPool().execute<ResultSetHeader>(sql, params);
  return result;
};
