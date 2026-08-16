import streamlit as st

st.set_page_config(page_title="Wavelength", page_icon="🎵", layout="wide")

# ---- Sample data ----
SONGS = [
    {"id": 1, "title": "Midnight Drive", "artist": "Nova Sky", "genre": "Pop", "duration": "3:12", "emoji": "🌙"},
    {"id": 2, "title": "Electric Pulse", "artist": "Voltage", "genre": "Electronic", "duration": "4:05", "emoji": "⚡"},
    {"id": 3, "title": "Stone Roads", "artist": "The Wanderers", "genre": "Rock", "duration": "3:48", "emoji": "🪨"},
    {"id": 4, "title": "City Lights", "artist": "Nova Sky", "genre": "Pop", "duration": "2:58", "emoji": "🌆"},
    {"id": 5, "title": "Rhythm & Rhyme", "artist": "MC Solace", "genre": "Hip-Hop", "duration": "3:30", "emoji": "🎤"},
    {"id": 6, "title": "Golden Hour", "artist": "Fern & Lune", "genre": "Indie", "duration": "3:20", "emoji": "🌇"},
    {"id": 7, "title": "Bassline Theory", "artist": "Voltage", "genre": "Electronic", "duration": "3:55", "emoji": "🔊"},
    {"id": 8, "title": "Backroad Anthem", "artist": "The Wanderers", "genre": "Rock", "duration": "4:22", "emoji": "🛣️"},
]
GENRES = ["Pop", "Rock", "Hip-Hop", "Electronic", "Indie"]

# ---- Session state ----
if "liked" not in st.session_state:
    st.session_state.liked = set()
if "queue" not in st.session_state:
    st.session_state.queue = []
if "now_playing" not in st.session_state:
    st.session_state.now_playing = None


def get_song(song_id):
    return next((s for s in SONGS if s["id"] == song_id), None)


# ---- Header ----
st.title("🎵 Wavelength")
st.caption("Your music, your mood — stream anything, anytime.")

section = st.sidebar.radio("Go to", ["Browse Songs", "Now Playing", "Liked Songs"])
st.sidebar.divider()
st.sidebar.metric("Songs liked", len(st.session_state.liked))
st.sidebar.metric("Songs in queue", len(st.session_state.queue))

st.divider()

# ---- Browse Songs ----
if section == "Browse Songs":
    col_search, col_genre = st.columns([2, 1])
    with col_search:
        search = st.text_input("Search songs or artists")
    with col_genre:
        genre_filter = st.selectbox("Genre", ["All"] + GENRES)

    songs = SONGS
    if genre_filter != "All":
        songs = [s for s in songs if s["genre"] == genre_filter]
    if search:
        term = search.lower()
        songs = [s for s in songs if term in s["title"].lower() or term in s["artist"].lower()]

    st.divider()
    for song in songs:
        with st.container(border=True):
            c1, c2, c3, c4, c5 = st.columns([1, 3, 2, 1, 1])
            c1.markdown(f"<span style='font-size:28px'>{song['emoji']}</span>", unsafe_allow_html=True)
            c2.markdown(f"**{song['title']}**  \n{song['artist']} · {song['genre']}")
            c3.caption(song["duration"])
            if c4.button("▶️", key=f"play_{song['id']}"):
                st.session_state.now_playing = song["id"]
                st.toast(f"Playing {song['title']}", icon="🎵")
            liked = song["id"] in st.session_state.liked
            if c5.button("❤️" if liked else "🤍", key=f"like_{song['id']}"):
                st.session_state.liked ^= {song["id"]}
                st.rerun()

# ---- Now Playing ----
elif section == "Now Playing":
    current = get_song(st.session_state.now_playing)
    if not current:
        st.info("Nothing playing. Go to **Browse Songs** and hit ▶️.", icon="🎵")
    else:
        st.markdown(f"<div style='font-size:70px; text-align:center'>{current['emoji']}</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center'>{current['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center'>{current['artist']} · {current['genre']}</p>", unsafe_allow_html=True)
        st.progress(0.4, text=f"1:12 / {current['duration']}")
        c1, c2, c3 = st.columns(3)
        c1.button("⏮️ Previous", use_container_width=True)
        c2.button("⏸️ Pause", use_container_width=True)
        if c3.button("⏭️ Next", use_container_width=True):
            if st.session_state.queue:
                st.session_state.now_playing = st.session_state.queue.pop(0)
                st.rerun()

    st.divider()
    st.markdown("### Up Next")
    if not st.session_state.queue:
        st.caption("Queue is empty.")
    for i, sid in enumerate(st.session_state.queue):
        s = get_song(sid)
        if s:
            st.write(f"{i + 1}. {s['emoji']} **{s['title']}** — {s['artist']}")

    with st.expander("➕ Add to queue"):
        options = {f"{s['title']} — {s['artist']}": s["id"] for s in SONGS}
        pick = st.selectbox("Song", list(options.keys()))
        if st.button("Add"):
            st.session_state.queue.append(options[pick])
            st.rerun()

# ---- Liked Songs ----
elif section == "Liked Songs":
    if not st.session_state.liked:
        st.info("No liked songs yet. Go to **Browse Songs** and tap 🤍.", icon="❤️")
    for sid in st.session_state.liked:
        song = get_song(sid)
        if song:
            c1, c2, c3 = st.columns([1, 4, 1])
            c1.markdown(f"<span style='font-size:24px'>{song['emoji']}</span>", unsafe_allow_html=True)
            c2.write(f"**{song['title']}** — {song['artist']}")
            if c3.button("▶️", key=f"liked_play_{sid}"):
                st.session_state.now_playing = sid
                st.toast(f"Playing {song['title']}", icon="🎵")
