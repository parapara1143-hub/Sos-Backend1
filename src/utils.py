
from flask import request
from math import ceil

def paginate(query, schema, default_page=1, default_size=20):
    page = int(request.args.get("page", default_page))
    size = int(request.args.get("size", default_size))
    items = query.paginate(page=page, per_page=size, error_out=False)
    return {
        "data": schema.dump(items.items, many=True),
        "page": page,
        "size": size,
        "total": items.total,
        "pages": ceil(items.total / size) if size else 1
    }
