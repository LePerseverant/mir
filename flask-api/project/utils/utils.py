from flask import request

def get_pagination_urls(limit: int, offset: int, total_count: int):
    base_url = request.base_url
    prev_offset = max(offset - limit, 0) if offset > 0 else None
    next_offset = offset + limit if offset + limit < total_count else None

    prev_url = f"{base_url}?limit={limit}&offset={prev_offset}" if prev_offset is not None else None
    next_url = f"{base_url}?limit={limit}&offset={next_offset}" if next_offset is not None else None

    return prev_url, next_url
