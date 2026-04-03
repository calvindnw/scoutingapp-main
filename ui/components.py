import streamlit as st
from textwrap import dedent


def render_html_block(content):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


def section_header(title, eyebrow=None, caption=None, centered=False):
    target = st
    if centered:
        left, middle, right = st.columns([1, 2.4, 1])
        target = middle

    if eyebrow:
        target.caption(str(eyebrow).upper())

    target.subheader(title)


def section_note(text):
    render_html_block(
        f"""
        <div class="alab-inline-note">{text}</div>
        """
    )


def kpi_card(title, value):
    render_html_block(
        f"""
        <div class="card alab-kpi">
            <div class="card-title alab-kpi-label">{title}</div>
            <div class="card-value alab-kpi-value">{value}</div>
        </div>
        """
    )

def player_card(name, age, position, club, nationality, photo_url):
    render_html_block(
        f"""
        <div class="alab-player-card">
            <img src="{photo_url}" class="alab-player-photo">
            <div>
                <div class="alab-player-name">{name} ({age})</div>
                <div class="alab-player-copy">{position} | {club} | {nationality}</div>
            </div>
        </div>
        """
    )
