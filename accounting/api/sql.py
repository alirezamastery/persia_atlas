SQL_INVOICE_ACTUAL_PRODUCT_COUNT = """
WITH
    serial_count AS (
        SELECT
            ap.id
          , ap.title
          , COUNT(DISTINCT ii.serial) AS "cnt"
        FROM
            accounting_invoice                 AS i
            INNER JOIN accounting_invoiceitem  AS ii
                       ON ii.invoice_id = i.id
            INNER JOIN products_productvariant AS v
                       ON v.dkpc = ii.dkpc
            INNER JOIN products_actualproduct  AS ap
                       ON v.actual_product_id = ap.id
        WHERE
            i.id = %(invoice_id)s
        GROUP BY
            ap.id, ap.title
        ORDER BY
            cnt DESC
    ),
    result AS (
        SELECT
            ROW_NUMBER() OVER (ORDER BY serial_count.cnt DESC) AS rnum
          , serial_count.*
        FROM
            serial_count
    )
SELECT *
FROM
        (TABLE result)                           AS res
        RIGHT JOIN (SELECT SUM(cnt) FROM result) AS c(total)
                   ON TRUE;
"""

SQL_ACTUAL_PRODUCT_SALES_BY_MONTH = """
WITH
    months_start AS (
        SELECT
            m                    AS month_start
          , ROW_NUMBER() OVER () AS num
        FROM
            UNNEST(%(months_start)s) AS m
    )
  , next_months_start AS (
    SELECT
        m                    AS next_month_start
      , ROW_NUMBER() OVER () AS num
    FROM
        UNNEST(%(next_months_start)s) AS m
)
  , date_ranges AS (
    SELECT
        ms.month_start
      , nms.next_month_start
    FROM
        months_start          AS ms
        INNER JOIN next_months_start AS nms
                   ON ms.num = nms.num
)
  , range_count AS (
    SELECT
        dr.month_start
      , COUNT(DISTINCT item.serial) AS cnt
    FROM
        accounting_invoiceitem             AS item
        INNER JOIN products_productvariant AS var
                   ON var.dkpc = item.dkpc
        INNER JOIN products_actualproduct  AS ap
                   ON var.actual_product_id = ap.id
        INNER JOIN date_ranges             AS dr
                   ON item.date >= dr.month_start AND item.date < dr.next_month_start
    WHERE
        ap.id = %(ap_id)s
    GROUP BY
        dr.month_start
)
  , result AS (
    SELECT
        dr.month_start
      , dr.next_month_start
      , COALESCE(range_count.cnt, 0) AS count
    FROM
        date_ranges AS dr
        LEFT JOIN range_count
                  ON dr.month_start = range_count.month_start
)
SELECT *
FROM
    result;
"""
