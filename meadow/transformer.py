"""
MEADOW Content Transformer Pipeline
Anomaly1911Writings | glennharlow/portable-ai-toolkit
Version: 1.0.0 | Born: July 5, 2026

Watches /vault for new poems, songs, books, and essays.
Transforms each piece into platform-ready posts for:
  YouTube, TikTok, Instagram, Facebook
Queues posts automatically and publishes via Ayrshare API.

INSTALL:
    pip install watchdog openai requests python-dotenv

USAGE:
    python transformer.py              # Scan vault then watch for changes
    python transformer.py --scan       # One-time scan of all vault files
    python transformer.py --publish    # Push queued posts to Ayrshare
    python transformer.py --queue      # Show current post queue
    python transformer.py --test FILE  # Test transform a specific file
"""

import os, json, time, logging, argparse, hashlib
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
CONFIG = {
    "VAULT_PATH":       Path(__file__).parent.parent / "vault",
    "QUEUE_PATH":       Path(__file__).parent / "queue",
    "LOG_FILE":         Path(__file__).parent / "logs" / "transformer.log",
    "AYRSHARE_API_KEY": os.getenv("AYRSHARE_API_KEY", ""),
    "OPENAI_API_KEY":   os.getenv("OPENAI_API_KEY", ""),
    "OWNER_NAME":       "Glenn",
    "BRAND":            "Anomaly1911Writings",
    "BRAND_HANDLE":     "@Anomaly1911Writings",
    "PLATFORMS":        ["youtube", "tiktok", "instagram", "facebook"],
    "SUPPORTED_EXTS":   {".txt", ".md", ".rtf"},
    "CATEGORIES":       ["poems", "songs", "books", "essays"],
    "AUTO_POST":        False,
    "MAX_CAPTION_LEN":  {
        "tiktok":    2200,
        "instagram": 2200,
        "facebook":  63206,
        "youtube":   5000,
    },
    "HASHTAG_SETS": {
        "poems": [
            "#poetry", "#poem", "#poet", "#poetrycommunity", "#spokenword",
            "#writersofinstagram", "#poetsofinstagram", "#wordsmith",
            "#creativewriting", "#poetrylovers", "#instapoetry", "#poems",
            "#writingcommunity", "#storytelling", "#lyricalpoetry",
            "#poetryisnotdead", "#blackpoetry", "#urbanpoetry", "#deepwords",
            "#originalpoetry", "#poetrylife", "#inspiration", "#motivational",
            "#Anomaly1911Writings", "#anomaly1911", "#glennharlow",
            "#artistsoninstagram", "#blackwriters", "#independentartist",
            "#selfexpression", "#authenticity"
        ],
        "songs": [
            "#newmusic", "#songwriter", "#lyrics", "#musicproducer",
            "#indieartist", "#hiphop", "#rap", "#spokenword", "#rnb",
            "#musicislife", "#originalmusic", "#unsignedartist", "#musiclovers",
            "#lyricism", "#bars", "#rap2026", "#independentmusic",
            "#recordingstudio", "#musicvideo", "#Anomaly1911Writings",
            "#anomaly1911", "#glennharlow", "#beatmaker", "#producerlife",
            "#newartist", "#risingartist", "#blackmusic", "#hiphopculture",
            "#raplyrics", "#musicianlife"
        ],
        "books": [
            "#amwriting", "#writerslife", "#authorsofinstagram", "#bookstagram",
            "#writingcommunity", "#booklover", "#newbook", "#indieauthor",
            "#selfpublished", "#fiction", "#storytelling", "#creativewriting",
            "#bookworm", "#readersofinstagram", "#authorlife", "#writingtips",
            "#Anomaly1911Writings", "#anomaly1911", "#glennharlow",
            "#blackauthors", "#blackwriters", "#independentauthor",
            "#booksofinstagram", "#literarylife", "#readingcommunity",
            "#writersofig", "#novelsofinstagram", "#bookish", "#booknerd",
            "#wordsofwisdom"
        ],
        "essays": [
            "#thoughts", "#opinion", "#perspective", "#deepthoughts",
            "#reflection", "#mindset", "#motivation", "#inspiration",
            "#realness", "#truth", "#wisdom", "#philosophy", "#growth",
            "#authenticity", "#blackthought", "#consciousness", "#awareness",
            "#Anomaly1911Writings", "#anomaly1911", "#glennharlow",
            "#writerscommunity", "#essayist", "#socialmedia", "#content",
            "#creator", "#contentcreator", "#digitalcreator",
            "#blackcreators", "#storytelling", "#voice"
        ],
    },
    "BRAND_SIGNATURES": {
        "poems":  "\n\n-- {brand} | Words by Glenn Harlow",
        "songs":  "\n\n-- {brand} | Original Lyrics by Glenn Harlow",
        "books":  "\n\n-- {brand} | Excerpt from an upcoming novel by Glenn Harlow",
        "essays": "\n\n-- {brand} | Written by Glenn Harlow",
    },
    "CHARITY_LINES": [
        "\n\nI collect pop tabs for RMHC. Drop them off, save a family.",
        "\n\nProudly supporting the Dave Thomas Foundati
# -- SETUP LOGGING ------------------------------------------------------------
Path(CONFIG["LOG_FILE"]).parent.mkdir(parents=True, exist_ok=True)
Path(CONFIG["QUEUE_PATH"]).mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] TRANSFORMER :: %(message)s",
    handlers=[
        logging.FileHandler(CONFIG["LOG_FILE"]),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("transformer")

if OPENAI_AVAILABLE and CONFIG["OPENAI_API_KEY"]:
    openai.api_key = CONFIG["OPENAI_API_KEY"]


# -- CATEGORY DETECTION -------------------------------------------------------
def detect_category(file_path: Path) -> str:
    for part in file_path.parts:
        if part.lower() in CONFIG["CATEGORIES"]:
            return part.lower()
    text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
    if any(w in text for w in ["verse", "stanza", "rhyme", "chorus"]):
        return "poems"
    if any(w in text for w in ["hook", "bridge", "beat", "melody"]):
        return "songs"
    if any(w in text for w in ["chapter", "prologue", "epilogue"]):
        return "books"
    return "essays"


# -- AI FORMATTER -------------------------------------------------------------
def ai_format(content: str, category: str, platform: str) -> str:
    if not OPENAI_AVAILABLE or not CONFIG["OPENAI_API_KEY"]:
        return fallback_format(content, category, platform)
    platform_guides = {
        "tiktok":    "TikTok caption: punchy, 1-3 sentences, strong hook",
        "instagram": "Instagram caption: emotional, 3-5 sentences, invites comments",
        "facebook":  "Facebook post: warm and personal, 2-4 sentences, invites sharing",
        "youtube":   "YouTube description: SEO-friendly, 3-5 sentences, ends with subscribe CTA",
    }
    prompt = (
        f"You are the content manager for {CONFIG['BRAND']}, the creative brand of Glenn Harlow "
        f"-- poet, songwriter, and author from Missouri. "
        f"Transform this {category.rstrip('s')} into a {platform_guides.get(platform, 'social post')}. "
        f"Keep Glenn's authentic, real voice. Do NOT add hashtags. "
        f"Content:\n\n{content[:1500]}"
    )
    try:
        resp = openai.OpenAI().chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300, temperature=0.8,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        log.warning(f"OpenAI format failed ({e}). Using fallback.")
        return fallback_format(content, category, platform)


def fallback_format(content: str, category: str, platform: str) -> str:
    lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
    if not lines: return content[:500]
    if platform == "tiktok":    return " ".join(lines[:3
# -- HASHTAG BUILDER ---------------------------------------------------------
def build_hashtags(category: str, platform: str) -> str:
    tags = CONFIG["HASHTAG_SETS"].get(category, CONFIG["HASHTAG_SETS"]["essays"])
    counts = {"tiktok": 30, "instagram": 25, "facebook": 5, "youtube": 10}
    n = min(counts.get(platform, 15), len(tags))
    return "\n\n" + " ".join(tags[:n])


# -- QUEUE MANAGEMENT --------------------------------------------------------
def load_queue() -> list:
    if CONFIG["QUEUE_FILE"].exists():
        return json.loads(CONFIG["QUEUE_FILE"].read_text())
    return []

def save_queue(queue: list):
    CONFIG["QUEUE_FILE"].write_text(json.dumps(queue, indent=2))

def load_processed() -> dict:
    if CONFIG["PROCESSED_FILE"].exists():
        return json.loads(CONFIG["PROCESSED_FILE"].read_text())
    return {}

def save_processed(processed: dict):
    CONFIG["PROCESSED_FILE"].write_text(json.dumps(processed, indent=2))

def add_to_queue(posts: list):
    queue = load_queue()
    queue.extend(posts)
    save_queue(queue)
    log.info(f"Added {len(posts)} posts to queue. Total queued: {len(queue)}")


# -- POST BUILDER ------------------------------------------------------------
def build_post(content: str, category: str, platform: str, file_name: str) -> dict:
    caption   = ai_format(content, category, platform)
    signature = CONFIG["BRAND_SIGNATURES"].get(category, "").format(brand=CONFIG["BRAND"])
    hashtags  = build_hashtags(category, platform)
    processed = load_processed()
    charity   = CONFIG["CHARITY_LINES"][len(processed) % len(CONFIG["CHARITY_LINES"])] \
                if len(processed) % 5 == 0 else ""
    full_text = caption + signature + charity + hashtags
    max_len   = CONFIG["MAX_CAPTION_LEN"].get(platform, 2000)
    if len(full_text) > max_len:
        overhead  = len(signature + charity + hashtags)
        caption   = caption[:max_len - overhead - 10] + "..."
        full_text = caption + signature + charity + hashtags
    post = {
        "id":         hashlib.md5(f"{file_name}{platform}{datetime.now().isoformat()}".encode()).hexdigest()[:12],
        "file":       file_name,
        "category":   category,
        "platform":   platform,
        "text":       full_text,
        "created_at": datetime.now().isoformat(),
        "status":     "queued",
        "char_count": len(full_text),
    }
# -- AYRSHARE PUBLISHER ------------------------------------------------------
class AyrsharePublisher:
    BASE_URL = "https://app.ayrshare.com/api"
    def __init__(self):
        self.key     = CONFIG["AYRSHARE_API_KEY"]
        self.headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
    def is_ready(self) -> bool:
        return bool(self.key) and "YOUR_" not in self.key
    def post(self, post: dict) -> dict:
        if not self.is_ready():
            log.warning("Ayrshare key not set. Post queued but not published.")
            return {"status": "queued_no_key"}
        payload = {"post": post["text"], "platforms": [post["platform"]]}
        if post["platform"] == "youtube" and "title" in post:
            payload["youTubeOptions"] = {"title": post["title"], "tags": post.get("tags", [])}
        try:
            r = requests.post(f"{self.BASE_URL}/post", headers=self.headers, json=payload, timeout=30)
            result = r.json()
            log.info(f"Ayrshare [{post['platform']}]: {result.get('status', 'unknown')}")
            return result
        except Exception as e:
            log.error(f"Ayrshare post failed: {e}")
            return {"status": "error", "error": str(e)}


# -- CONTENT TRANSFORMER ------------------------------------------------------
class ContentTransformer:
    def __init__(self):
        self.publisher = AyrsharePublisher()

    def transform_file(self, file_path: Path) -> list:
        if file_path.suffix.lower() not in CONFIG["SUPPORTED_EXTS"]:
            return []
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        except Exception as e:
            log.error(f"Could not read {file_path}: {e}"); return []
        if len(content) < 10:
            log.warning(f"Skipping {file_path.name} -- too short."); return []
        category = detect_category(file_path)
        log.info(f"Transforming: {file_path.name} [{category}]")
        posts = []
        for platform in CONFIG["PLATFORMS"]:
            post = build_post(content, category, platform, file_path.name)
            posts.append(post)
            log.info(f"  [{platform}] {post['char_count']} chars")
        processed = load_processed()
        file_hash  = hashlib.md5(content.encode()).hexdigest()
        processed[str(file_path)] = {
            "hash": file_hash, "processed_at": datetime.now().isoformat(),
            "category": category, "posts_built": len(posts),
        }
        save_processed(processed)
        return posts

    def scan_vault(self) -> list:
        vault = Path(CONFIG["VAULT_PATH"])
        if not vault.exists():
            log.warning(f"Vault not found at {vault}. Run: .\\meadow_run.ps1 -Action setup")
            return []
        processed = load_processed()
        all_posts  = []
        for ext in CONFIG["SUPPORTED_EXTS"]:
            for f in vault.rglob(f"*{ext}"):
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore").strip()
                except Exception:
                    continue
                file_hash = hashlib.md5(content.encode()).hexdigest()
                if processed.get(str(f), {}).get("hash") == file_hash:
                    log.info(f"Unchanged: {f.name} -- skipping."); continue
                posts = self.transform_file(f)
                all_posts.extend(posts)
        if all_posts:
            add_to_queue(all_posts)
        log.info(f"Scan complete. {len(all_posts)} new posts queued.")
        return all_posts

    def process_queue(self):
        queue   = load_queue()
        pending = [p for p in queue if p.get("status") == "queued"]
        if not pending:
            log.info("Queue is empty."); return
        if not self.publisher.is_ready():
            log.warning(f"{len(pending)} posts queued. Set AYRSHARE_API_KEY in .env then run --publish.")
            return
        for post in pending:
            result = self.publisher.post(post)
            post["status"]       = "published" if result.get("status") == "success" else "failed"
            post["published_at"] = datetime.now().isoformat()
            post["result"]       = result
            time.sleep(1)
        save_queue(queue)
        ok = sum(1 for p in pending if p["status"] == "published")
        log.info(f"Published {ok}/{len(pending)} posts.")

    def show_queue(self):
        queue = load_queue()
        if not queue:
            print("\n  Queue is empty. Run --scan to transform vault content.\n"); return
        by_status = {}
        for p in queue:
            by_status.setdefault(p.get("status", "unknown"), []).append(p)
        print(f"\n  MEADOW Post Queue -- {datetime.now().strftime('%A, %B %d, %Y')}")
        print(f"  Total: {len(queue)} posts\n")
        for status, posts in by_status.items():
            print(f"  {status.upper():<12} {len(posts)}")
        print("\n  Recent queued:")
        for p in [x for x in queue if x.get("status") == "queued"][:8]:
            print(f"    [{p['platform']:<10}] [{p['category']:<8}] {p['file']} ({p['char_count']} chars)")
        print()

    def test_file(self, file_path: str):
        f = Path(file_path)
        if not f.exists():
            print(f"  File not found: {file_path}"); return
        posts = self.transform_file(f)
        if not posts:
            print("  No posts generated."); return
        print(f"\n  TEST TRANSFORM -- {f.name} [{detect_category(f)}]")
        for post in posts:
            print(f"\n  [{post['platform'].upper()}] {post['char_count']} chars")
            print(f"  {post['text'][:300]}...")
        print()

    if platform == "youtube":
        post["title"] = content.splitlines()[0][:100] if content.strip() else file_name
        post["tags"]  = [t.lstrip("#") for t in build_hashtags(category, "youtube").split()
                         if t.startswith("#")][:15]
    return post
])[:280]
    elif platform == "instagram": return "\n".join(lines[:5])[:800]
    elif platform == "facebook":  return "\n".join(lines[:8])
    elif platform == "youtube":
        return f"{lines[0][:100]}\n\n{' '.join(lines[1:6])}\n\nFollow {CONFIG['BRAND_HANDLE']} for more."
    return content[:500]
on for Adoption.",
    ],
}

CONFIG["QUEUE_FILE"]     = CONFIG["QUEUE_PATH"] / "post_queue.json"
CONFIG["PROCESSED_FILE"] = CONFIG["QUEUE_PATH"] / "processed.json"

    WATCHDOG_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv(Path(__file__).parent / ".env")

# -- VAULT WATCHER ------------------------------------------------------------
class VaultWatcher(FileSystemEventHandler):
    def __init__(self, transformer):
        self.transformer = transformer
        self._cooldown   = {}

    def on_modified(self, event): self._handle(event)
    def on_created(self, event):  self._handle(event)

    def _handle(self, event):
        if event.is_directory: return
        path = Path(event.src_path)
        if path.suffix.lower() not in CONFIG["SUPPORTED_EXTS"]: return
        now = time.time()
        if now - self._cooldown.get(str(path), 0) < 5: return
        self._cooldown[str(path)] = now
        log.info(f"Vault change: {path.name}")
        time.sleep(1)
        posts = self.transformer.transform_file(path)
        if posts:
            add_to_queue(posts)
            if CONFIG["AUTO_POST"]:
                self.transformer.process_queue()


def start_watcher(transformer):
    if not WATCHDOG_AVAILABLE:
        log.error("watchdog not installed. Run: pip install watchdog"); return
    vault = Path(CONFIG["VAULT_PATH"])
    vault.mkdir(parents=True, exist_ok=True)
    observer = Observer()
    observer.schedule(VaultWatcher(transformer), str(vault), recursive=True)
    observer.start()
    log.info(f"Watching vault at {vault}")
    log.info("Drop a .txt or .md into vault/poems, vault/songs, vault/books, or vault/essays")
    log.info("MEADOW will transform it into 4 platform posts automatically.")
    log.info("Press Ctrl+C to stop.\n")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# -- MAIN ---------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="MEADOW Content Transformer -- Anomaly1911Writings")
    p.add_argument("--scan",    action="store_true")
    p.add_argument("--publish", action="store_true")
    p.add_argument("--queue",   action="store_true")
    p.add_argument("--test",    metavar="FILE")
    args = p.parse_args()
    t = ContentTransformer()
    print(f"\n  MEADOW Content Transformer v1.0 | {CONFIG['BRAND']}")
    print(f"  {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}\n")
    if   args.queue:   t.show_queue()
    elif args.scan:    t.scan_vault()
    elif args.publish: t.process_queue()
    elif args.test:    t.test_file(args.test)
    else:
        t.scan_vault()
        start_watcher(t)

if __name__ == "__main__":
    main()
