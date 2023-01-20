-- create date ranges from month start and end
WITH
    start_month AS (
        SELECT MIN(DATE_TRUNC('month', item.date)) FROM accounting_invoiceitem AS item
    ),
    end_month AS (
        SELECT MAX(DATE_TRUNC('month', item.date)) FROM accounting_invoiceitem AS item
    ),
    months AS (
        SELECT
                    (SELECT * FROM start_month) + (INTERVAL '1' MONTH * GENERATE_SERIES(0, month_count::INT)) AS month
        FROM
            (
                SELECT
                    EXTRACT(YEAR FROM diff) * 12 + EXTRACT(MONTH FROM diff) AS month_count
                FROM
                    (
                        SELECT AGE((SELECT * FROM end_month), (SELECT * FROM start_month)) AS diff
                    ) td
            ) t
    ),
    date_ranges AS (
        SELECT
            m.month                                         AS month_start
          , LEAD(m.month, 1, NOW()) OVER (ORDER BY m.month) AS month_end
        FROM
            months AS m
    )
SELECT *
FROM date_ranges

-- create month series
SELECT
        DATE '2008-01-01' + (INTERVAL '1' MONTH * GENERATE_SERIES(0, month_count::INT))
FROM
    (
        SELECT
            EXTRACT(YEAR FROM diff) * 12 + EXTRACT(MONTH FROM diff) AS month_count
        FROM
            (
                SELECT AGE(CURRENT_TIMESTAMP, TIMESTAMP '2008-01-01 00:00:00') AS diff
            ) td
    ) t


-- create date month date range
SELECT
    m.month                                                           AS month_start
  , LEAD(m.month::DATE, 1, NOW()::DATE) OVER (ORDER BY m.month::DATE) AS month_end
FROM
    months AS m