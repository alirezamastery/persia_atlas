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
