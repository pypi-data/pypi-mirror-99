BEGIN TRANSACTION;
--------------------------------------------------------------------------------
PRAGMA foreign_keys = 0;

--------------------------------------------------------------------------------
-- Reclassify bond coupons in dividends table
--------------------------------------------------------------------------------
UPDATE dividends
   SET type = 2
 WHERE id IN (
    SELECT d.id
      FROM dividends AS d
           LEFT JOIN
           assets AS a ON d.asset_id = a.id
     WHERE a.type_id = 3
);

--------------------------------------------------------------------------------
-- Move coupons from 'trades' table into 'dividends
--------------------------------------------------------------------------------
INSERT INTO dividends (
                          timestamp,
                          number,
                          type,
                          account_id,
                          asset_id,
                          sum,
                          sum_tax,
                          note
                      )
                      SELECT timestamp,
                             number,
                             2,
                             account_id,
                             asset_id,
                             iif(qty > 0, -coupon, coupon),
                             0,
                             "НКД"
                        FROM trades
                       WHERE coupon != 0;


--------------------------------------------------------------------------------
-- Rename fields in 'dividends' table: 'sum'->'amount', 'sum_tax'->'tax
--------------------------------------------------------------------------------
CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM dividends;

DROP TABLE dividends;

CREATE TABLE dividends (
    id         INTEGER     PRIMARY KEY
                           UNIQUE
                           NOT NULL,
    timestamp  INTEGER     NOT NULL,
    ex_date    INTEGER,
    number     TEXT (32)   DEFAULT (''),
    type       INTEGER     NOT NULL,
    account_id INTEGER     REFERENCES accounts (id) ON DELETE CASCADE
                                                    ON UPDATE CASCADE
                           NOT NULL,
    asset_id   INTEGER     REFERENCES assets (id) ON DELETE RESTRICT
                                                  ON UPDATE CASCADE
                           NOT NULL,
    amount     REAL        NOT NULL
                           DEFAULT (0),
    tax        REAL        DEFAULT (0),
    note       TEXT (1014)
);

INSERT INTO dividends (
                          id,
                          timestamp,
                          ex_date,
                          number,
                          type,
                          account_id,
                          asset_id,
                          amount,
                          tax,
                          note
                      )
                      SELECT id,
                             timestamp,
                             ex_date,
                             number,
                             type,
                             account_id,
                             asset_id,
                             sum,
                             sum_tax,
                             note
                        FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

CREATE TRIGGER dividends_after_delete
         AFTER DELETE
            ON dividends
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

CREATE TRIGGER dividends_after_insert
         AFTER INSERT
            ON dividends
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

CREATE TRIGGER dividends_after_update
         AFTER UPDATE OF timestamp,
                         account_id,
                         asset_id,
                         amount,
                         tax
            ON dividends
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;


--------------------------------------------------------------------------------
-- Drop field 'coupon' from 'trades' table
--------------------------------------------------------------------------------
CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM trades;

DROP TABLE trades;

CREATE TABLE trades (
    id         INTEGER     PRIMARY KEY
                           UNIQUE
                           NOT NULL,
    timestamp  INTEGER     NOT NULL,
    settlement INTEGER     DEFAULT (0),
    number     TEXT (32)   DEFAULT (''),
    account_id INTEGER     REFERENCES accounts (id) ON DELETE CASCADE
                                                    ON UPDATE CASCADE
                           NOT NULL,
    asset_id   INTEGER     REFERENCES assets (id) ON DELETE RESTRICT
                                                  ON UPDATE CASCADE
                           NOT NULL,
    qty        REAL        NOT NULL
                           DEFAULT (0),
    price      REAL        NOT NULL
                           DEFAULT (0),
    fee        REAL        DEFAULT (0),
    note       TEXT (1024)
);

INSERT INTO trades (
                       id,
                       timestamp,
                       settlement,
                       number,
                       account_id,
                       asset_id,
                       qty,
                       price,
                       fee,
                       note
                   )
                   SELECT id,
                          timestamp,
                          settlement,
                          number,
                          account_id,
                          asset_id,
                          qty,
                          price,
                          fee,
                          note
                     FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

CREATE TRIGGER trades_after_delete
         AFTER DELETE
            ON trades
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp;
END;

CREATE TRIGGER trades_after_insert
         AFTER INSERT
            ON trades
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= NEW.timestamp;
END;

CREATE TRIGGER trades_after_update
         AFTER UPDATE OF timestamp,
                         account_id,
                         asset_id,
                         qty,
                         price,
                         fee
            ON trades
      FOR EACH ROW
BEGIN
    DELETE FROM ledger
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM sequence
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
    DELETE FROM ledger_sums
          WHERE timestamp >= OLD.timestamp OR
                timestamp >= NEW.timestamp;
END;

--------------------------------------------------------------------------------
-- Update 'all_transactions' view - remove 'coupon' field
--------------------------------------------------------------------------------
DROP VIEW all_transactions;

CREATE VIEW all_transactions AS
    SELECT at.*,
           a.currency_id AS currency
      FROM (
               SELECT 1 AS type,
                      a.id,
                      a.timestamp,
                      CASE WHEN SUM(d.sum) < 0 THEN -COUNT(d.sum) ELSE COUNT(d.sum) END AS subtype,
                      a.account_id AS account,
                      NULL AS asset,
                      SUM(d.sum) AS amount,
                      d.category_id AS category,
                      NULL AS price,
                      NULL AS fee_tax,
                      a.peer_id AS peer,
                      d.tag_id AS tag
                 FROM actions AS a
                      LEFT JOIN
                      action_details AS d ON a.id = d.pid
                GROUP BY a.id
               UNION ALL
               SELECT 2 AS type,
                      d.id,
                      d.timestamp,
                      d.type AS subtype,
                      d.account_id AS account,
                      d.asset_id AS asset,
                      d.amount AS amount,
                      NULL AS category,
                      NULL AS price,
                      d.tax AS fee_tax,
                      a.organization_id AS peer,
                      NULL AS tag
                 FROM dividends AS d
                      LEFT JOIN
                      accounts AS a ON a.id = d.account_id
               UNION ALL
               SELECT 5 AS type,
                      a.id,
                      a.timestamp,
                      a.type AS subtype,
                      a.account_id AS account,
                      a.asset_id AS asset,
                      a.qty AS amount,
                      NULL AS category,
                      a.qty_new AS price,
                      a.basis_ratio AS fee_tax,
                      a.asset_id_new AS peer,
                      NULL AS tag
                 FROM corp_actions AS a
               UNION ALL
               SELECT 3 AS type,
                      t.id,
                      t.timestamp,
                      iif(t.qty < 0, -1, 1) AS subtype,
                      t.account_id AS account,
                      t.asset_id AS asset,
                      t.qty AS amount,
                      NULL AS category,
                      t.price AS price,
                      t.fee AS fee_tax,
                      a.organization_id AS peer,
                      NULL AS tag
                 FROM trades AS t
                      LEFT JOIN
                      accounts AS a ON a.id = t.account_id
               UNION ALL
               SELECT 4 AS type,
                      id,
                      withdrawal_timestamp AS timestamp,
-                     1 AS subtype,
                      withdrawal_account AS account,
                      asset AS asset,
                      withdrawal AS amount,
                      NULL AS category,
                      NULL AS price,
                      NULL AS fee_tax,
                      NULL AS peer,
                      NULL AS tag
                 FROM transfers AS t
               UNION ALL
               SELECT 4 AS type,
                      id,
                      withdrawal_timestamp AS timestamp,
                      0 AS subtype,
                      fee_account AS account,
                      asset AS asset,
                      fee AS amount,
                      NULL AS category,
                      NULL AS price,
                      NULL AS fee_tax,
                      NULL AS peer,
                      NULL AS tag
                 FROM transfers AS t
                WHERE NOT fee_account IS NULL
               UNION ALL
               SELECT 4 AS type,
                      id,
                      deposit_timestamp AS timestamp,
                      1 AS subtype,
                      deposit_account AS account,
                      asset AS asset,
                      deposit AS amount,
                      NULL AS category,
                      NULL AS price,
                      NULL AS fee_tax,
                      NULL AS peer,
                      NULL AS tag
                 FROM transfers AS t
                ORDER BY timestamp,
                         type,
                         subtype,
                         id
           )
           AS at
           LEFT JOIN
           accounts AS a ON at.account = a.id;

-----------------------------------------------------------------------------------
-- Update view 'all_operations' to include 'subtype' field from 'dividends' table
-----------------------------------------------------------------------------------
DROP VIEW all_operations;
CREATE VIEW all_operations AS
    SELECT m.type,
           m.subtype,
           m.id,
           m.timestamp,
           m.account_id,
           a.name AS account,
           m.num_peer,
           m.asset_id,
           s.name AS asset,
           s.full_name AS asset_name,
           m.note,
           m.note2,
           m.amount,
           m.qty_trid,
           m.price,
           m.fee_tax,
           iif(coalesce(money.sum_amount, 0) > 0, money.sum_amount, coalesce(debt.sum_amount, 0) ) AS t_amount,
           m.t_qty,
           c.name AS currency,
           CASE WHEN m.timestamp <= a.reconciled_on THEN 1 ELSE 0 END AS reconciled
      FROM (
               SELECT 1 AS type,
                      iif(SUM(d.sum) < 0, -1, 1) AS subtype,
                      o.id,
                      timestamp,
                      p.name AS num_peer,
                      account_id,
                      sum(d.sum) AS amount,
                      o.alt_currency_id AS asset_id,
                      NULL AS qty_trid,
                      sum(d.alt_sum) AS price,
                      NULL AS fee_tax,
                      NULL AS t_qty,
                      NULL AS note,
                      NULL AS note2
                 FROM actions AS o
                      LEFT JOIN
                      agents AS p ON o.peer_id = p.id
                      LEFT JOIN
                      action_details AS d ON o.id = d.pid
                GROUP BY o.id
               UNION ALL
               SELECT 2 AS type,
                      d.type AS subtype,
                      d.id,
                      d.timestamp,
                      d.number AS num_peer,
                      d.account_id,
                      d.amount AS amount,
                      d.asset_id,
                      SUM(coalesce(l.amount, 0) ) AS qty_trid,
                      NULL AS price,
                      d.tax AS fee_tax,
                      NULL AS t_qty,
                      d.note AS note,
                      c.name AS note2
                 FROM dividends AS d
                      LEFT JOIN
                      ledger AS l ON d.asset_id = l.asset_id AND
                                     d.account_id = l.account_id AND
                                     l.book_account = 4 AND
                                     l.timestamp <= d.timestamp
                      LEFT JOIN
                      assets AS a ON d.asset_id = a.id
                      LEFT JOIN
                      countries AS c ON a.country_id = c.id
                GROUP BY d.id
               UNION ALL
               SELECT 5 AS type,
                      ca.type AS subtype,
                      ca.id,
                      ca.timestamp,
                      ca.number AS num_peer,
                      ca.account_id,
                      ca.qty AS amount,
                      ca.asset_id,
                      ca.qty_new AS qty_trid,
                      ca.basis_ratio AS price,
                      ca.type AS fee_tax,
                      l.sum_amount AS t_qty,
                      a.name AS note,
                      a.full_name AS note2
                 FROM corp_actions AS ca
                      LEFT JOIN
                      assets AS a ON ca.asset_id_new = a.id
                      LEFT JOIN
                      sequence AS q ON q.type = 5 AND
                                       ca.id = q.operation_id
                      LEFT JOIN
                      ledger_sums AS l ON l.sid = q.id AND
                                          l.asset_id = ca.asset_id_new AND
                                          l.book_account = 4
               UNION ALL
               SELECT 3 AS type,
                      iif(t.qty < 0, -1, 1) AS subtype,
                      t.id,
                      t.timestamp,
                      t.number AS num_peer,
                      t.account_id,
-                     (t.price * t.qty) AS amount,
                      t.asset_id,
                      t.qty AS qty_trid,
                      t.price AS price,
                      t.fee AS fee_tax,
                      l.sum_amount AS t_qty,
                      t.note AS note,
                      NULL AS note2
                 FROM trades AS t
                      LEFT JOIN
                      sequence AS q ON q.type = 3 AND
                                       t.id = q.operation_id
                      LEFT JOIN
                      ledger_sums AS l ON l.sid = q.id AND
                                          l.book_account = 4
               UNION ALL
               SELECT 4 AS type,
                      t.subtype,
                      t.id,
                      t.timestamp,
                      c.name AS num_peer,
                      t.account_id,
                      t.amount,
                      NULL AS asset_id,
                      NULL AS qty_trid,
                      t.rate AS price,
                      NULL AS fee_tax,
                      NULL AS t_qty,
                      t.note,
                      a.name AS note2
                 FROM (
                          SELECT id,
                                 withdrawal_timestamp AS timestamp,
                                 withdrawal_account AS account_id,
                                 deposit_account AS account2_id,
-                                withdrawal AS amount,
                                 deposit / withdrawal AS rate,
-                                1 AS subtype,
                                 note
                            FROM transfers
                          UNION ALL
                          SELECT id,
                                 withdrawal_timestamp AS timestamp,
                                 fee_account AS account_id,
                                 NULL AS account2_id,
-                                fee AS amount,
                                 1 AS rate,
                                 0 AS subtype,
                                 note
                            FROM transfers
                           WHERE NOT fee IS NULL
                          UNION ALL
                          SELECT id,
                                 deposit_timestamp AS timestamp,
                                 deposit_account AS account_id,
                                 withdrawal_account AS account2_id,
                                 deposit AS amount,
                                 withdrawal / deposit AS rate,
                                 1 AS subtype,
                                 note
                            FROM transfers
                           ORDER BY id
                      )
                      AS t
                      LEFT JOIN
                      accounts AS a ON a.id = t.account2_id
                      LEFT JOIN
                      assets AS c ON c.id = a.currency_id
                ORDER BY timestamp
           )
           AS m
           LEFT JOIN
           accounts AS a ON m.account_id = a.id
           LEFT JOIN
           assets AS s ON m.asset_id = s.id
           LEFT JOIN
           assets AS c ON a.currency_id = c.id
           LEFT JOIN
           sequence AS q ON m.type = q.type AND
                            m.subtype = q.subtype AND
                            m.id = q.operation_id
           LEFT JOIN
           ledger_sums AS money ON money.sid = q.id AND
                                   money.account_id = m.account_id AND
                                   money.book_account = 3
           LEFT JOIN
           ledger_sums AS debt ON debt.sid = q.id AND
                                  debt.account_id = m.account_id AND
                                  debt.book_account = 5;

--------------------------------------------------------------------------------

PRAGMA foreign_keys = 1;

--------------------------------------------------------------------------------
-- Set new DB schema version
UPDATE settings SET value=17 WHERE name='SchemaVersion';

COMMIT;