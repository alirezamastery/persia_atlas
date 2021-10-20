def get_variant_search_url(dkpc):
    return f'https://seller.digikala.com/ajax/variants/search/?sortColumn=&' \
           f'sortOrder=desc&page=1&items=10&search[type]=product_variant_id&search[value]={dkpc}&'