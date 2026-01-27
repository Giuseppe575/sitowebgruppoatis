import json
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from feeds_config import FEEDS_AMBIENTE, FEEDS_SICUREZZA

CACHE_TTL_SECONDS = 15 * 60
REQUEST_TIMEOUT_SECONDS = 6
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "feeds.json")
CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", ".cache", "feeds_cache.json")


def _safe_text(elem):
    if elem is None or elem.text is None:
        return ""
    return elem.text.strip()


def _parse_date(value):
    if not value:
        return None
    value = value.strip()
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc)
    except Exception:
        pass
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    except Exception:
        return None


def _find_first(elem, tag_end):
    for child in list(elem):
        if child.tag.endswith(tag_end):
            return child
    return None


def _find_all(elem, tag_end):
    return [c for c in list(elem) if c.tag.endswith(tag_end)]


def _get_link_from_atom(entry):
    for link in _find_all(entry, "link"):
        href = link.attrib.get("href", "").strip()
        rel = link.attrib.get("rel", "").strip()
        if href and rel != "self":
            return href
    return ""


def _get_link_from_rss(item):
    link = _find_first(item, "link")
    return _safe_text(link)


def _source_name_from_root(root, fallback_url):
    if root.tag.endswith("rss") or root.tag.endswith("RDF"):
        channel = _find_first(root, "channel")
        title = _safe_text(_find_first(channel, "title")) if channel is not None else ""
    else:
        title = _safe_text(_find_first(root, "title"))
    if title:
        return title
    host = urllib.parse.urlparse(fallback_url).netloc
    return host or "Fonte"


def _parse_feed(xml_bytes, feed_url):
    root = ET.fromstring(xml_bytes)
    source_name = _source_name_from_root(root, feed_url)
    items = []

    if root.tag.endswith("feed"):
        for entry in _find_all(root, "entry"):
            title = _safe_text(_find_first(entry, "title"))
            url = _get_link_from_atom(entry)
            published = _safe_text(_find_first(entry, "published")) or _safe_text(_find_first(entry, "updated"))
            published_dt = _parse_date(published)
            if not url:
                continue
            items.append(
                {
                    "title": title or "Senza titolo",
                    "url": url,
                    "publishedAtISO": published_dt.isoformat().replace("+00:00", "Z")
                    if published_dt
                    else "",
                    "sourceName": source_name,
                    "_publishedDt": published_dt,
                }
            )
    else:
        channel = _find_first(root, "channel")
        for item in _find_all(channel, "item") if channel is not None else []:
            title = _safe_text(_find_first(item, "title"))
            url = _get_link_from_rss(item)
            published = _safe_text(_find_first(item, "pubDate")) or _safe_text(_find_first(item, "date"))
            published_dt = _parse_date(published)
            if not url:
                continue
            items.append(
                {
                    "title": title or "Senza titolo",
                    "url": url,
                    "publishedAtISO": published_dt.isoformat().replace("+00:00", "Z")
                    if published_dt
                    else "",
                    "sourceName": source_name,
                    "_publishedDt": published_dt,
                }
            )

    return items


def _load_cache():
    if not os.path.exists(CACHE_PATH):
        return {"fetchedAtByUrl": {}, "itemsByUrl": {}}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"fetchedAtByUrl": {}, "itemsByUrl": {}}


def _save_cache(cache):
    cache_dir = os.path.dirname(CACHE_PATH)
    os.makedirs(cache_dir, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def _fetch_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ATIS Feed Builder"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        return resp.read()


def _collect_items(urls, cache):
    now = time.time()
    items = []

    for url in urls:
        cached_at = cache["fetchedAtByUrl"].get(url, 0)
        cached_items = cache["itemsByUrl"].get(url, [])
        if now - cached_at < CACHE_TTL_SECONDS and cached_items:
            items.extend(cached_items)
            continue

        try:
            xml_bytes = _fetch_feed(url)
            parsed_items = _parse_feed(xml_bytes, url)
            cache["fetchedAtByUrl"][url] = now
            cache["itemsByUrl"][url] = parsed_items
            items.extend(parsed_items)
        except Exception:
            if cached_items:
                items.extend(cached_items)

    return items


def _normalize(items, limit):
    dedup = {}
    for item in items:
        if item["url"] in dedup:
            continue
        dedup[item["url"]] = item

    def sort_key(it):
        return it.get("_publishedDt") or datetime(1970, 1, 1, tzinfo=timezone.utc)

    ordered = sorted(dedup.values(), key=sort_key, reverse=True)[:limit]
    for it in ordered:
        it.pop("_publishedDt", None)
    return ordered


def main():
    cache = _load_cache()

    sicurezza_items = _collect_items(FEEDS_SICUREZZA, cache)
    ambiente_items = _collect_items(FEEDS_AMBIENTE, cache)

    data = {
        "generatedAtISO": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "topics": {
            "sicurezza": _normalize(sicurezza_items, 10),
            "ambiente": _normalize(ambiente_items, 10),
        },
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    _save_cache(cache)


if __name__ == "__main__":
    main()
