import streamlit as st
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_css():
    css_file = PROJECT_ROOT / "dashboard" / "style.css"

    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as file:
            st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def page_header(title, subtitle, show_live=True):
    """Title + subtitle + LIVE badge, matching the top of the reference dashboard."""

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown(f'<div class="dashboard-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dashboard-subtitle">{subtitle}</div>', unsafe_allow_html=True)

    with col2:
        if show_live:
            st.markdown('<div class="live-indicator">&#9679; LIVE</div>', unsafe_allow_html=True)


def kpi_card(title, value, description=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def chart_card_title(text):
    """Title shown INSIDE a bordered chart card, above the plotly chart."""
    st.markdown(f'<div class="chart-card-title">{text}</div>', unsafe_allow_html=True)


def status_badge(status):
    status_clean = str(status).lower()

    if status_clean == "delivered":
        css_class = "badge-delivered"
    elif status_clean == "cancelled":
        css_class = "badge-cancelled"
    elif status_clean == "pending":
        css_class = "badge-pending"
    else:
        css_class = "badge-default"

    return f'<span class="status-badge {css_class}">{status}</span>'
