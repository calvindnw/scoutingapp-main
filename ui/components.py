import streamlit as st
from textwrap import dedent


def render_html_block(content):
    st.markdown(dedent(content).strip(), unsafe_allow_html=True)


def section_header(title, eyebrow=None, caption=None, centered=False):
    align_class = " alab-block-header-center" if centered else ""
    eyebrow_html = f"<div class='alab-block-eyebrow'>{eyebrow}</div>" if eyebrow else ""
    render_html_block(
        f"""
        <div class="alab-block-header{align_class}">
            {eyebrow_html}
            <div class="alab-block-title">{title}</div>
        </div>
        """
    )


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
