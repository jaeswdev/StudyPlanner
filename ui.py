"""Pixel-adventure HUD styling for the Study Planner."""

import base64
from pathlib import Path

import streamlit as st


def apply_elemental_theme() -> None:
    """Turn the Streamlit controls into a compact pixel-adventure HUD."""
    styles = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Press+Start+2P&display=swap');
    :root { --ink: #112e4c; --ocean: #245f91; --sky: #779bdf; --ice: #e9f9fb; --white: #fffdf5; --gold: #ffd45f; --gold-light: #fff0a7; }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background: #789ddd !important; }
    .block-container { width: min(720px, calc(100vw - 3rem)) !important; box-sizing: border-box; margin-left: auto; margin-right: auto; padding: 2rem 1.5rem 5rem; background: #eaf8fb !important; border: 4px solid var(--ink); box-shadow: 9px 9px 0 rgba(17,46,76,.75), inset 0 0 0 4px rgba(255,255,255,.7); overflow: visible; }
    h1, h2, h3 { font-family: 'Press Start 2P', monospace !important; color: var(--ink) !important; line-height: 1.5 !important; }
    h1 { font-size: clamp(1.55rem, 4vw, 2.35rem) !important; text-shadow: 3px 3px 0 #b5e4ed; }
    h2, h3 { font-size: 1rem !important; }
    p, label, .stCaption, .stMarkdown { font-family: 'DM Sans', sans-serif; color: var(--ink); }
    [data-testid="stCaptionContainer"] p { color: #205d83 !important; font-weight: 700; }
    [data-testid="stSidebar"] { background: rgba(18,58,95,.96); border-right: 4px solid #c4edf2; }
    [data-testid="stSidebar"] * { color: var(--white) !important; }
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a { border: 2px solid transparent; border-radius: 0; margin: 6px 8px; padding: 10px 8px; }
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover, [data-testid="stSidebar"] [aria-selected="true"] { background: #397eac; border-color: #d3f4f4; box-shadow: 3px 3px 0 #0b2741; }
    div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stVerticalBlockBorderWrapper"] > div { background: #fffdf5 !important; border: 3px solid var(--ink) !important; border-radius: 0 !important; box-shadow: 5px 5px 0 rgba(17,46,76,.45), inset 0 0 0 3px #d4f0f3; }
    div[data-testid="stForm"] { padding: 1.25rem; }
    [data-testid="stVerticalBlockBorderWrapper"] { border: 4px solid var(--ink) !important; border-radius: 0 !important; margin: .85rem 0 !important; background: #fffdf5 !important; box-shadow: 6px 6px 0 rgba(17,46,76,.55) !important; }
    [data-testid="stVerticalBlockBorderWrapper"] > div { padding: .8rem .9rem !important; }
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] { align-items: center; }
    [data-testid="stVerticalBlockBorderWrapper"] p { margin-bottom: .35rem !important; }
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p { color: #3c769b !important; font-size: .93rem !important; }
    [data-testid="stVerticalBlockBorderWrapper"] code { display: inline-block; background: #153c65 !important; border: 2px solid #0b2945; border-radius: 0 !important; box-shadow: 2px 2px 0 #7ac3d7; color: #f8fdf8 !important; font-family: 'Press Start 2P', monospace !important; font-size: .58rem !important; line-height: 1.55 !important; padding: .35rem .42rem; white-space: nowrap; }
    .quest-title { color: #112e4c; font-size: 1.12rem; font-weight: 700; line-height: 1.3; margin-bottom: .5rem; }
    .course-chip { display: inline-block; background: #d7f0f3; border: 2px solid #397eac; box-shadow: 2px 2px 0 #397eac; color: #153c65; font-family: 'DM Sans', sans-serif; font-size: .78rem; font-weight: 800; letter-spacing: .04em; line-height: 1.4; padding: .28rem .55rem; text-transform: uppercase; }
    .quest-meta { color: #3d769a; font-size: .93rem; font-weight: 700; margin-top: .7rem; }
    .status-label { color: #3c769b; font-size: .68rem; font-weight: 800; letter-spacing: .12em; margin-bottom: .25rem; }
    .status-badge { display: inline-block; border: 2px solid #112e4c; box-shadow: 2px 2px 0 #112e4c; font-family: 'DM Sans', sans-serif; font-size: .78rem; font-weight: 800; line-height: 1.4; padding: .3rem .5rem; white-space: nowrap; }
    .status-done { background: #9fe6b4; color: #154d2c; }
    .status-in-progress { background: #a8dff0; color: #174d79; }
    .status-not-started { background: #f4dfa0; color: #67480a; }
    .progress-card { background: #fffdf5; border: 3px solid var(--ink); box-shadow: 5px 5px 0 rgba(17,46,76,.45); margin: 1rem 0 1.35rem; padding: .85rem 1rem 1rem; }
    .progress-label { color: var(--ink); display: flex; font-size: .86rem; font-weight: 800; justify-content: space-between; margin-bottom: .55rem; }
    .progress-label strong { color: #397eac; }
    .progress-track { background: #d7f0f3; border: 2px solid var(--ink); height: 14px; overflow: hidden; }
    .progress-fill { background: #65bf87; border-right: 2px solid #154d2c; height: 100%; min-width: 0; }
    .scroll-top { align-items: center; background: var(--gold); border: 3px solid var(--ink); bottom: 1.5rem; box-shadow: 4px 4px 0 var(--ink); color: var(--ink) !important; display: flex; flex-direction: column; font-family: 'Press Start 2P', monospace; font-size: .7rem; gap: .15rem; justify-content: center; line-height: 1; min-height: 3.2rem; padding: .35rem .55rem; position: fixed; right: 1.5rem; text-decoration: none !important; width: 3.2rem; z-index: 60; }
    .scroll-top:hover { background: #ffea8b; color: var(--ink) !important; transform: translate(2px,2px); box-shadow: 2px 2px 0 var(--ink); }
    .scroll-top span { font-family: 'DM Sans', sans-serif; font-size: .58rem; font-weight: 800; letter-spacing: .05em; }
    .collision-badge { display: inline-block; background: #f6b68b; border: 2px solid #8e3d23; color: #69270f; font-family: 'Press Start 2P', monospace; font-size: .5rem; padding: .25rem .33rem; margin-left: .45rem; }
    .companion { position: fixed; z-index: 50; width: 152px; padding: .5rem; background: rgba(234,248,251,.94); border: 3px solid #112e4c; box-shadow: 5px 5px 0 rgba(17,46,76,.7); text-align: center; }
    .companion-left { left: 1.2rem; bottom: 1.5rem; }
    .companion-right { right: 1.2rem; bottom: 1.5rem; }
    .companion img { display: block; width: 100%; max-height: 138px; object-fit: contain; image-rendering: pixelated; }
    .companion p { margin: .45rem .1rem .1rem; color: #153c65; font-family: 'Press Start 2P', monospace; font-size: .52rem; line-height: 1.7; }
    .stTextInput input, .stNumberInput input, [data-baseweb="select"] > div, [data-baseweb="input"] > div { background: #fffef8 !important; border: 3px solid #397eac !important; border-radius: 0 !important; color: var(--ink) !important; font-weight: 600 !important; }
    .stButton button, .stFormSubmitButton button, button[data-testid^="stBaseButton"] { background: var(--gold) !important; color: #112e4c !important; border: 3px solid var(--ink) !important; border-radius: 0 !important; box-shadow: 5px 5px 0 var(--ink), inset 0 0 0 2px var(--gold-light); font-family: 'Press Start 2P', monospace !important; font-size: .68rem !important; font-weight: 700 !important; line-height: 1.8 !important; min-height: 3rem !important; padding: .62rem .9rem !important; text-shadow: none !important; }
    .stButton button:hover, .stFormSubmitButton button:hover, button[data-testid^="stBaseButton"]:hover { background: #ffea8b !important; transform: translate(2px,2px); box-shadow: 3px 3px 0 var(--ink), inset 0 0 0 2px #fff8c9; }
    .stButton button:active, .stFormSubmitButton button:active, button[data-testid^="stBaseButton"]:active { transform: translate(5px,5px); box-shadow: none; }
    [data-testid="stButton"] { margin-top: .3rem; }
    [data-testid="stPageLink"] a { display: flex !important; justify-content: center; align-items: center; min-height: 3rem; box-sizing: border-box; background: var(--gold) !important; color: #112e4c !important; border: 3px solid var(--ink) !important; border-radius: 0 !important; box-shadow: 4px 4px 0 var(--ink), inset 0 0 0 2px var(--gold-light); font-family: 'Press Start 2P', monospace !important; font-size: .62rem !important; font-weight: 700 !important; text-decoration: none !important; }
    [data-testid="stPageLink"] a:hover { background: #ffea8b !important; color: #112e4c !important; transform: translate(2px,2px); box-shadow: 2px 2px 0 var(--ink), inset 0 0 0 2px #fff8c9; }
    [data-testid="stPageLink"] a p { color: #112e4c !important; font-family: 'Press Start 2P', monospace !important; font-size: .62rem !important; }
    [data-testid="stAlert"] { border: 3px solid var(--ink); border-radius: 0; box-shadow: 4px 4px 0 rgba(17,46,76,.3); }
    hr { border-color: #397eac !important; border-width: 2px !important; }
    .element-mark { display: inline-block; background: #c6edf1; border: 2px solid var(--ink); box-shadow: 3px 3px 0 var(--ink); color: var(--ink); font-family: 'Press Start 2P', monospace; font-size: .6rem; line-height: 1.6; padding: .38rem .5rem; text-transform: uppercase; }
    .welcome-card { background: rgba(35,100,147,.95); border: 4px solid var(--ink); border-radius: 0; box-shadow: 7px 7px 0 var(--ink); color: var(--white); padding: 1.3rem; margin: 1.2rem 0; }
    .welcome-card h2, .welcome-card p { color: var(--white) !important; }
    .welcome-card h2 { margin: 0 0 .65rem !important; }
    .element-pill { display: inline-block; border: 2px solid #d9f7f6; padding: .25rem .48rem; margin: .18rem .25rem 0 0; font-size: .82rem; font-weight: 700; }
    .hud-rule { height: 8px; margin: .75rem 0 1.15rem; background: repeating-linear-gradient(90deg, #153c65 0 14px, #7ec5d9 14px 21px); border: 2px solid #153c65; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width: 0 !important; }
    @media (max-width: 1050px) { .companion { display: none; } }
    @media (max-width: 700px) { .block-container { width: calc(100vw - 1.2rem) !important; margin: 0 .6rem; padding: 1.35rem 1rem 3rem; } .progress-label { font-size: .78rem; } .scroll-top { bottom: 1rem; right: .8rem; } }
    </style>
    """
    st.markdown(styles, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### STUDY QUEST")
        st.caption("Choose your next move.")


def page_intro(mark: str, title: str, subtitle: str) -> None:
    st.markdown('<div id="planner-top"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="element-mark">{mark}</div>', unsafe_allow_html=True)
    st.title(title)
    st.caption(subtitle)
    st.markdown('<div class="hud-rule"></div>', unsafe_allow_html=True)


def show_task_companions(incomplete: int, complete: int) -> None:
    """Show margin companions that reflect the current task balance."""
    if incomplete >= 7:
        left = ("fire.jpg", "The quest list is growing. Choose your next move.")
        right = ("party.jpg", "One clear task at a time. You can turn this around.")
    elif complete and complete >= incomplete:
        left = ("air.gif", "Great momentum. Keep the wind at your back.")
        right = ("momo.jpg", "A lighter quest log means time for a small victory.")
    elif complete:
        left = ("water.jpg", "Steady progress beats rushing. Keep going.")
        right = ("toph.jpg", "Stay grounded. Finish the next small quest.")
    else:
        left = ("sleepy.jpg", "Your quests are waiting. Start with the easiest one.")
        right = ("air2.gif", "A small step now makes tomorrow easier.")

    def image_data(filename: str) -> tuple[str, str]:
        path = Path(__file__).parent / "assets" / "companions" / filename
        mime = "image/gif" if path.suffix == ".gif" else "image/jpeg"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return mime, data

    left_mime, left_data = image_data(left[0])
    right_mime, right_data = image_data(right[0])
    st.markdown(
        f'''<aside class="companion companion-left"><img alt="Progress companion" src="data:{left_mime};base64,{left_data}"><p>{left[1]}</p></aside>
        <aside class="companion companion-right"><img alt="Progress companion" src="data:{right_mime};base64,{right_data}"><p>{right[1]}</p></aside>''',
        unsafe_allow_html=True,
    )
