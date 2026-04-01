import requests
import streamlit as st

# ─── CONFIG ───────────────────────────────────────────────────────────────────
API_BASE  = "http://127.0.0.1:8000"
TMDB_IMG  = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CinePulse",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
.block-container {
    padding-top: 4rem !important;
    padding-bottom: 3rem !important;
    max-width: 1440px !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid #1f1f1f;
}
section[data-testid="stSidebar"] * {
    color: #e5e5e5 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: transparent;
    border: 1px solid #2a2a2a;
    color: #e5e5e5 !important;
    border-radius: 8px;
    width: 100%;
    transition: all .2s;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: .02em;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #1a1a1a;
    border-color: #e5194b;
    color: #fff !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label {
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: .08em;
    color: #777 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #1f1f1f;
}

/* ── Page background ── */
.stApp {
    background: #0a0a0a;
}

/* ── Hero title ── */
.hero-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    color: #f5f5f5;
    letter-spacing: -.02em;
    line-height: 1.05;
    margin: 0 0 .3rem;
}
.hero-title span { color: #e5194b; }
.hero-sub {
    color: #555;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: .02em;
    margin-bottom: 1.6rem;
}

/* ── Search box ── */
.stTextInput input {
    background: #141414 !important;
    border: 1.5px solid #252525 !important;
    border-radius: 12px !important;
    color: #f0f0f0 !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color .2s !important;
}
.stTextInput input:focus {
    border-color: #e5194b !important;
    box-shadow: 0 0 0 3px rgba(229,25,75,.12) !important;
}
.stTextInput label {
    color: #666 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: .08em;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #141414 !important;
    border-color: #252525 !important;
    color: #f0f0f0 !important;
    border-radius: 10px !important;
}

/* ── Section labels ── */
.section-label {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.45rem;
    color: #f0f0f0;
    letter-spacing: -.01em;
    margin: 1.6rem 0 .8rem;
    display: flex;
    align-items: center;
    gap: .45rem;
}
.section-label .badge {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    background: #e5194b;
    color: #fff;
    padding: 2px 8px;
    border-radius: 20px;
    letter-spacing: .06em;
    text-transform: uppercase;
    vertical-align: middle;
}

/* ── Movie card ── */
.movie-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: #141414;
    border: 1px solid #1c1c1c;
    transition: transform .22s ease, box-shadow .22s ease;
    cursor: pointer;
}
.movie-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 18px 40px rgba(0,0,0,.6), 0 0 0 1px #e5194b44;
}
.movie-card img {
    display: block;
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
}
.movie-card .no-poster {
    aspect-ratio: 2/3;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1a1a1a;
    font-size: 2.5rem;
}
.movie-card .card-info {
    padding: 10px 10px 12px;
}
.movie-card .card-title {
    font-size: 0.82rem;
    font-weight: 500;
    color: #e5e5e5;
    line-height: 1.25;
    max-height: 2.5rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
.movie-card .open-btn {
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,.55);
    align-items: center;
    justify-content: center;
}
.movie-card:hover .open-btn { display: flex; }
.open-btn-label {
    background: #e5194b;
    color: #fff;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 7px 18px;
    border-radius: 20px;
    letter-spacing: .04em;
    pointer-events: none;
}

/* ── Streamlit buttons on grid ── */
div[data-testid="column"] .stButton > button {
    width: 100%;
    background: rgba(229,25,75,.85) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: .04em;
    padding: 6px 0 !important;
    margin-top: 4px !important;
    transition: background .18s !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: #c0143f !important;
}

/* ── Details page ── */
.detail-card {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 18px;
    padding: 2rem 2.2rem;
}
.detail-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: clamp(1.6rem, 4vw, 2.6rem);
    color: #f5f5f5;
    letter-spacing: -.02em;
    margin-bottom: .4rem;
}
.detail-meta {
    color: #666;
    font-size: 0.85rem;
    font-weight: 400;
    margin-bottom: .25rem;
    letter-spacing: .01em;
}
.detail-meta strong { color: #aaa; font-weight: 500; }
.detail-overview {
    color: #bbb;
    font-size: 0.95rem;
    line-height: 1.65;
    margin-top: .8rem;
}

/* ── Divider ── */
hr[data-testid="stDivider"] {
    border-color: #1a1a1a !important;
}

/* ── Info / error messages ── */
.stAlert { border-radius: 10px !important; }

/* ── Slider ── */
.stSlider [data-baseweb="slider"] { margin-top: 4px; }

/* ── Streamlit images (poster in details) ── */
img[data-testid="stImage"] { border-radius: 14px; }

/* ── Backdrop ── */
.backdrop-wrap img { border-radius: 14px; opacity: .85; }
</style>
""", unsafe_allow_html=True)


# ─── STATE + ROUTING ──────────────────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id   = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"]   = str(int(tmdb_id))


# ─── API HELPERS ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=30, show_spinner=False)
def _fetch(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"

def api_get_json(path: str, params: dict | None = None):
    return _fetch(path, params)


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to display.")
        return
    rows = (len(cards) + cols - 1) // cols
    idx  = 0
    for r in range(rows):
        col_set = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m       = cards[idx]; idx += 1
            tmdb_id = m.get("tmdb_id")
            title   = m.get("title", "Untitled")
            poster  = m.get("poster_url")
            with col_set[c]:
                if poster:
                    st.image(poster, width=200)
                else:
                    st.markdown(
                        "<div style='aspect-ratio:2/3;background:#1a1a1a;border-radius:10px;"
                        "display:flex;align-items:center;justify-content:center;"
                        "font-size:2rem;color:#333;margin-bottom:4px'>🎞️</div>",
                        unsafe_allow_html=True,
                    )
                if tmdb_id:
                    if st.button("▶ Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                        goto_details(tmdb_id)
                st.markdown(
                    f"<div style='font-size:0.78rem;color:#ccc;line-height:1.2;"
                    f"height:2.4rem;overflow:hidden;display:-webkit-box;"
                    f"-webkit-line-clamp:2;-webkit-box-orient:vertical;margin-top:2px'>"
                    f"{title}</div>",
                    unsafe_allow_html=True,
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id":    tmdb["tmdb_id"],
                "title":      tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
            })
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title      = (m.get("title") or "").strip()
            tmdb_id    = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id    = m.get("tmdb_id") or m.get("id")
            title      = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id":      int(tmdb_id),
                "title":        title,
                "poster_url":   poster_url,
                "release_date": m.get("release_date", ""),
            })
    else:
        return [], []

    matched    = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year  = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='font-family:\"DM Serif Display\",serif;font-size:1.6rem;"
        "color:#f5f5f5;letter-spacing:-.02em;padding:0.6rem 0 0.2rem'>"
        "Cine<span style='color:#e5194b'>Pulse</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='color:#444;font-size:0.72rem;letter-spacing:.08em;"
        "text-transform:uppercase;margin-bottom:1rem'>Movie Recommender</div>",
        unsafe_allow_html=True,
    )
    st.button("🏠  Home", on_click=goto_home)
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.7rem;color:#555;text-transform:uppercase;"
        "letter-spacing:.1em;margin-bottom:6px'>Home Feed Category</div>",
        unsafe_allow_html=True,
    )
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
    )
    st.markdown(
        "<div style='font-size:0.7rem;color:#555;text-transform:uppercase;"
        "letter-spacing:.1em;margin:12px 0 4px'>Grid Columns</div>",
        unsafe_allow_html=True,
    )
    grid_cols = st.slider("Grid columns", 3, 8, 6, label_visibility="collapsed")
    st.markdown("---")


# ─── HERO HEADER ─────────────────────────────────────────────────────────────
st.markdown(
    "<div class='hero-title'>Discover your next<br><span>favourite film.</span></div>"
    "<div class='hero-sub'>Search · Explore · Get Recommendations</div>",
    unsafe_allow_html=True,
)
st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
#  VIEW: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.view == "home":

    typed = st.text_input(
        "SEARCH",
        placeholder="Search a movie title — e.g. Inception, Batman, Parasite…",
        label_visibility="visible",
    )

    # ── SEARCH MODE ──────────────────────────────────────────────────────────
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
            st.stop()

        data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})
        if err or data is None:
            st.error(f"Search failed: {err}")
            st.stop()

        suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip(), limit=24)

        if suggestions:
            labels   = ["— Select a title to jump to details —"] + [s[0] for s in suggestions]
            selected = st.selectbox("Quick select", labels, index=0, label_visibility="collapsed")
            if selected != labels[0]:
                label_to_id = {s[0]: s[1] for s in suggestions}
                goto_details(label_to_id[selected])
        else:
            st.info("No matching suggestions — showing closest results below.")

        st.markdown(
            f"<div class='section-label'>Search Results "
            f"<span class='badge'>{len(cards)} found</span></div>",
            unsafe_allow_html=True,
        )
        poster_grid(cards, cols=grid_cols, key_prefix="search_results")
        st.stop()

    # ── HOME FEED MODE ────────────────────────────────────────────────────────
    label_map = {
        "trending":    ("🔥", "Trending Now"),
        "popular":     ("⭐", "Popular"),
        "top_rated":   ("🏆", "Top Rated"),
        "now_playing": ("🎬", "Now Playing"),
        "upcoming":    ("🗓️", "Coming Soon"),
    }
    icon, label = label_map.get(home_category, ("🎬", home_category.replace("_", " ").title()))
    st.markdown(
        f"<div class='section-label'>{icon} {label}</div>",
        unsafe_allow_html=True,
    )

    home_cards, err = api_get_json("/home", params={"category": home_category, "limit": 24})
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")


# ═══════════════════════════════════════════════════════════════════════════════
#  VIEW: DETAILS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # ── Top bar ──────────────────────────────────────────────────────────────
    back_col, _ = st.columns([1, 5])
    with back_col:
        if st.button("← Back"):
            goto_home()

    # ── Fetch data ───────────────────────────────────────────────────────────
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # ── Layout: poster + info ─────────────────────────────────────────────────
    left, right = st.columns([1, 2.6], gap="large")

    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], width=320)
        else:
            st.markdown(
                "<div style='aspect-ratio:2/3;background:#141414;border-radius:14px;"
                "display:flex;align-items:center;justify-content:center;"
                "font-size:3.5rem;color:#2a2a2a;max-width:320px'>🎞️</div>",
                unsafe_allow_html=True,
            )

    with right:
        genres  = ", ".join([g["name"] for g in data.get("genres", [])]) or "—"
        release = data.get("release_date") or "—"
        rating  = data.get("vote_average")

        st.markdown(f"<div class='detail-title'>{data.get('title','')}</div>", unsafe_allow_html=True)

        rating_html = ""
        if rating:
            stars = "★" * round(rating / 2) + "☆" * (5 - round(rating / 2))
            rating_html = (
                f"<span style='color:#e5c419;font-size:0.95rem;letter-spacing:.04em'>{stars}</span>"
                f" <span style='color:#777;font-size:0.82rem'>({rating:.1f}/10)</span>"
            )

        st.markdown(
            f"<div class='detail-meta' style='margin-bottom:.6rem'>{rating_html}</div>"
            f"<div class='detail-meta'><strong>Release</strong>&nbsp;&nbsp;{release}</div>"
            f"<div class='detail-meta'><strong>Genres</strong>&nbsp;&nbsp;{genres}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<hr style='border-color:#1e1e1e;margin:1rem 0'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='detail-overview'>{data.get('overview') or 'No overview available.'}</div>",
            unsafe_allow_html=True,
        )

    # ── Backdrop ──────────────────────────────────────────────────────────────
    if data.get("backdrop_url"):
        st.markdown("<div style='margin-top:1.5rem'>", unsafe_allow_html=True)
        st.image(data["backdrop_url"], width=None)
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ── Recommendations ───────────────────────────────────────────────────────
    st.markdown(
        "<div class='section-label'>✨ Recommendations</div>",
        unsafe_allow_html=True,
    )

    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding recommendations…"):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )
        if not err2 and bundle:
            st.markdown(
                "<div class='section-label' style='font-size:1.1rem'>🔎 Similar Movies </div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )
            genre_movies = bundle.get("genre_recommendations", [])

            if genre_movies:
                st.markdown(
                    "<div class='section-label' style='font-size:1.1rem'>🎭 More Like This</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(genre_movies)
        else:
            st.info("Showing genre-based recommendations.")
            with st.spinner("Loading genre recommendations…"):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="details_genre_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")