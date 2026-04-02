import streamlit as st


def section_header(title, eyebrow=None, caption=None, centered=False):
    align_class = " alab-block-header-center" if centered else ""
    eyebrow_html = f"<div class='alab-block-eyebrow'>{eyebrow}</div>" if eyebrow else ""
    caption_html = f"<div class='alab-block-copy'>{caption}</div>" if caption else ""
    st.markdown(
        f"""
        <div class="alab-block-header{align_class}">
            {eyebrow_html}
            <div class="alab-block-title">{title}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_note(text):
    st.markdown(
        f"""
        <div class="alab-inline-note">{text}</div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(title, value):
    st.markdown(
        f"""
        <div class="card alab-kpi">
            <div class="card-title alab-kpi-label">{title}</div>
            <div class="card-value alab-kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def player_card(name, age, position, club, nationality, photo_url):
    st.markdown(
        f"""
        <div class="alab-player-card">
            <img src="{photo_url}" class="alab-player-photo">
            <div>
                <div class="alab-player-name">{name} ({age})</div>
                <div class="alab-player-copy">{position} | {club} | {nationality}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
