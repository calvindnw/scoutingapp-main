import streamlit as st


def load_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        :root {
            --bg-0: #0a1a14;
            --bg-1: #1a3a2a;
            --bg-2: #3a6651;
            --brand: #5a9a7c;
            --brand-soft: rgba(90, 154, 124, 0.14);
            --brand-line: rgba(90, 154, 124, 0.3);
            --panel-top: rgba(27, 51, 42, 0.86);
            --panel-bottom: rgba(10, 26, 20, 0.94);
            --text-1: rgba(255, 255, 255, 0.96);
            --text-2: rgba(226, 236, 231, 0.82);
            --text-3: rgba(193, 208, 200, 0.62);
            --warning: #ffd700;
            --radius-lg: 18px;
            --radius-md: 14px;
            --shadow-lg: 0 22px 64px rgba(0, 0, 0, 0.38);
            --shadow-md: 0 14px 36px rgba(0, 0, 0, 0.28);
            --shadow-sm: 0 10px 24px rgba(0, 0, 0, 0.2);
            --primary-color: #5a9a7c !important;
            --primary-color-hover: #5a9a7c !important;
        }

        html,
        body,
        [class*="css"] {
            font-family: 'Manrope', sans-serif;
        }

        body {
            color: var(--text-1);
            text-rendering: optimizeLegibility;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 14%, rgba(90, 154, 124, 0.16), transparent 34%),
                radial-gradient(circle at 84% 24%, rgba(58, 102, 81, 0.24), transparent 30%),
                linear-gradient(135deg, #3a6651 0%, #1a3a2a 44%, #0a1a14 100%);
            background-attachment: fixed;
            color: var(--text-1);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1480px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: var(--text-1) !important;
            font-family: 'Sora', sans-serif !important;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }

        p,
        li,
        label,
        .stMarkdown,
        .stCaption {
            color: var(--text-2) !important;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(58, 102, 81, 0.12), transparent 16%),
                linear-gradient(180deg, #0a1a14, #173126);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] .stMarkdown {
            color: var(--text-1) !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: linear-gradient(180deg, rgba(90, 154, 124, 0.22), rgba(58, 102, 81, 0.2));
            color: var(--text-1);
            font-weight: 700;
            box-shadow: var(--shadow-sm);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            border-color: var(--brand-line);
            background: linear-gradient(180deg, rgba(90, 154, 124, 0.32), rgba(58, 102, 81, 0.28));
        }

        .panel-title {
            color: var(--brand) !important;
            font-family: 'Sora', sans-serif !important;
            font-weight: 700;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 0.2rem 0 0.55rem;
            text-align: center;
        }

        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.7rem;
        }

        .kpi-card,
        .card,
        .rank-card,
        .player-card {
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: var(--shadow-md);
            overflow: hidden;
        }

        .kpi-card,
        .card {
            background:
                linear-gradient(180deg, rgba(30, 60, 114, 0.12), transparent 44%),
                linear-gradient(140deg, rgba(58, 102, 81, 0.9), rgba(10, 26, 20, 0.96));
            border-radius: var(--radius-lg);
        }

        .kpi-card {
            padding: 1.15rem 1.15rem 1rem;
        }

        .kpi-title,
        .card-title {
            color: var(--text-3) !important;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .kpi-value,
        .card-value {
            margin-top: 0.5rem;
            color: var(--text-1) !important;
            font-family: 'Sora', sans-serif !important;
            font-size: 1.95rem;
            font-weight: 800;
            line-height: 1.05;
        }

        .rank-card {
            background: linear-gradient(120deg, rgba(58, 102, 81, 0.86), rgba(10, 26, 20, 0.94));
            border-radius: var(--radius-md);
            padding: 0.85rem 1rem;
            margin-bottom: 0.55rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow-sm);
        }

        .rank-left {
            display: flex;
            gap: 0.8rem;
            align-items: center;
        }

        .rank-num {
            color: var(--warning);
            font-family: 'Sora', sans-serif !important;
            font-weight: 800;
            width: 34px;
            text-align: center;
        }

        .rank-name {
            color: var(--text-1) !important;
            font-size: 0.92rem;
            font-weight: 700;
        }

        .rank-score {
            color: var(--brand) !important;
            font-family: 'Sora', sans-serif !important;
            font-weight: 800;
            font-size: 1rem;
        }

        .player-card {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            width: 100%;
            min-height: 82px;
            margin: 0.35rem auto;
            padding: 0.85rem 0.95rem;
            background: linear-gradient(130deg, rgba(58, 102, 81, 0.88), rgba(10, 26, 20, 0.95));
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
        }

        .player-photo {
            width: 56px;
            height: 56px;
            border-radius: 16px;
            object-fit: cover;
            border: 1px solid rgba(90, 154, 124, 0.55);
        }

        .player-info h5 {
            margin: 0 0 0.18rem;
            color: var(--text-1) !important;
            font-family: 'Sora', sans-serif !important;
            font-size: 0.88rem;
            font-weight: 700;
        }

        .player-info p {
            margin: 0.08rem 0;
            color: var(--text-3) !important;
            font-size: 0.77rem;
        }

        .player-link a {
            color: var(--brand) !important;
            font-size: 0.74rem;
            font-weight: 700;
            text-decoration: none;
        }

        .line-title {
            color: var(--brand) !important;
            font-family: 'Sora', sans-serif !important;
            font-weight: 700;
            font-size: 0.95rem;
            letter-spacing: 0.03em;
            margin: 0.1rem 0 0.6rem;
            text-align: center;
        }

        .card {
            width: 100%;
            min-height: 146px;
            padding: 0.95rem 1rem;
            color: var(--text-1);
        }

        .card h5 {
            color: var(--text-1) !important;
            font-family: 'Sora', sans-serif !important;
            font-size: 0.94rem;
            margin: 0.2rem 0 0.35rem;
            text-align: left;
        }

        .card p {
            color: var(--text-2) !important;
            font-size: 0.81rem;
            margin: 0.16rem 0;
        }

        .card.visto {
            opacity: 0.85;
            background: linear-gradient(130deg, rgba(26, 31, 46, 0.92), rgba(42, 58, 90, 0.86));
        }

        .label {
            display: inline-flex;
            align-items: center;
            min-height: 24px;
            padding: 0.18rem 0.55rem;
            border-radius: 999px;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            margin-bottom: 0.55rem;
            text-transform: uppercase;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .vencido {
            background-color: rgba(139, 0, 0, 0.88);
            color: #ffffff;
        }

        .hoy {
            background-color: rgba(255, 215, 0, 0.94);
            color: #000000;
        }

        .proximo {
            background-color: rgba(0, 100, 0, 0.9);
            color: #ffffff;
        }

        .futuro {
            background-color: rgba(0, 68, 136, 0.88);
            color: #ffffff;
        }

        @media (max-width: 1024px) {
            .kpi-container {
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )