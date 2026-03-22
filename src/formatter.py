import re

def clean_title(title):
    return re.sub(r'[^a-zA-Z0-9 ]', '', title.lower())


def keyword_density(title, query):
    title_words = clean_title(title).split()
    query_words = query.lower().split()

    if not title_words:
        return 0

    match_count = sum(1 for word in title_words if word in query_words)
    return match_count / len(title_words)


def is_quality_title(title):
    # Remove clickbait / low-quality patterns
    bad_patterns = ["!!!", "??", "shocking", "must watch", "crazy"]

    title_lower = title.lower()
    return not any(pattern in title_lower for pattern in bad_patterns)


def calculate_score(title, views, query):
    score = 0

    # Normalize views (log scale to reduce domination)
    import math
    score += math.log10(views + 1) * 5

    # Keyword density weight
    density = keyword_density(title, query)
    score += density * 50

    return round(score, 2)


def format_video_data(videos, query, min_views=10000):
    seen_titles = set()
    formatted = []

    for video in videos:
        views = video.get("view_count") or 0
        title = video.get("title") or ""

        if not title or views < min_views:
            continue

        # Remove duplicates
        if title in seen_titles:
            continue
        seen_titles.add(title)

        # Filter low-quality titles
        if not is_quality_title(title):
            continue

        score = calculate_score(title, views, query)

        formatted.append({
            "title": title,
            "uploader": video.get("uploader"),
            "views": views,
            "score": score,
            "url": f"https://www.youtube.com/watch?v={video.get('id')}",
            "thumbnail": f"https://img.youtube.com/vi/{video.get('id')}/hqdefault.jpg"
        })

    # Sort by score
    formatted.sort(key=lambda x: x["score"], reverse=True)

    return formatted

