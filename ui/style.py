import streamlit as st


def load_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        :root {
            --alab-bg-0: #081310;
            --alab-bg-1: #0f1d1a;
            --alab-bg-2: #163029;
            --alab-brand: #19e28f;
            --alab-brand-soft: rgba(25, 226, 143, 0.12);
            --alab-brand-line: rgba(25, 226, 143, 0.28);
            --alab-panel-top: rgba(19, 30, 27, 0.94);
            --alab-panel-bottom: rgba(8, 19, 16, 0.98);
            --alab-text-1: rgba(255, 255, 255, 0.96);
            --alab-text-2: rgba(221, 231, 227, 0.78);
            --alab-text-3: rgba(174, 190, 183, 0.58);
            --alab-warning: #f3bf4c;
            --alab-radius-lg: 22px;
            --alab-radius-md: 16px;
            --alab-radius-sm: 12px;
            --alab-shadow-lg: 0 30px 90px rgba(0, 0, 0, 0.42);
            --alab-shadow-md: 0 18px 44px rgba(0, 0, 0, 0.28);
            --alab-shadow-sm: 0 12px 28px rgba(0, 0, 0, 0.2);
        }

        .stApp {
            position: relative;
            background:
                radial-gradient(circle at 14% 10%, rgba(25, 226, 143, 0.1), transparent 30%),
                radial-gradient(circle at 82% 20%, rgba(39, 110, 82, 0.24), transparent 28%),
                linear-gradient(180deg, #264b3f 0%, #19372e 34%, #10231d 68%, #091511 100%);
            background-attachment: fixed;
            color: var(--alab-text-1);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                repeating-linear-gradient(
                    0deg,
                    rgba(255, 255, 255, 0.028) 0,
                    rgba(255, 255, 255, 0.028) 1px,
                    transparent 1px,
                    transparent 30px
                ),
                repeating-linear-gradient(
                    90deg,
                    rgba(255, 255, 255, 0.022) 0,
                    rgba(255, 255, 255, 0.022) 1px,
                    transparent 1px,
                    transparent 30px
                ),
                repeating-linear-gradient(
                    135deg,
                    rgba(255, 255, 255, 0.014) 0,
                    rgba(255, 255, 255, 0.014) 2px,
                    transparent 2px,
                    transparent 44px
                ),
                radial-gradient(circle at 20% 18%, rgba(255, 255, 255, 0.04), transparent 1px),
                radial-gradient(circle at 78% 32%, rgba(25, 226, 143, 0.05), transparent 1px);
            background-size: 30px 30px, 30px 30px, 44px 44px, 18px 18px, 24px 24px;
            opacity: 0.42;
            mix-blend-mode: screen;
            z-index: 0;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: transparent;
            position: relative;
            z-index: 1;
        }

        [data-testid="stHeader"] {
            background: linear-gradient(180deg, rgba(7, 14, 12, 0.98), rgba(7, 14, 12, 0.84));
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }

        [data-testid="stToolbar"] {
            right: 0.9rem;
            top: 0.35rem;
        }

        [data-testid="stToolbar"] button,
        [data-testid="stToolbar"] a,
        [data-testid="stToolbar"] svg,
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            color: rgba(255, 255, 255, 0.72) !important;
            fill: rgba(255, 255, 255, 0.72) !important;
        }

        [data-testid="stToolbar"] button:hover,
        [data-testid="stToolbar"] a:hover,
        [data-testid="stToolbar"] button:hover svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        [data-testid="stDecoration"] {
            background: linear-gradient(90deg, rgba(25, 226, 143, 0.78), rgba(25, 226, 143, 0.14));
            height: 2px;
        }

        .alab-dashboard-hero {
            position: relative;
            overflow: hidden;
            margin: 0.35rem 0 1.4rem;
            padding: 1.45rem 1.5rem 1.3rem;
            border-radius: 26px;
            border: 1px solid rgba(255, 255, 255, 0.09);
            background:
                radial-gradient(circle at top right, rgba(25, 226, 143, 0.13), transparent 28%),
                linear-gradient(145deg, rgba(20, 32, 29, 0.98), rgba(8, 19, 16, 0.98));
            box-shadow: var(--alab-shadow-lg);
        }

        .alab-dashboard-hero::before {
            content: "";
            position: absolute;
            inset: 0 auto auto 0;
            width: 160px;
            height: 2px;
            background: linear-gradient(90deg, rgba(25, 226, 143, 0.95), rgba(25, 226, 143, 0));
        }

        .alab-dashboard-hero-kicker {
            color: var(--alab-brand);
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }

        .alab-dashboard-hero-title {
            margin: 0;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: clamp(1.8rem, 3vw, 2.55rem);
            font-weight: 800;
            line-height: 1.02;
        }

        .alab-dashboard-hero-copy {
            max-width: 760px;
            margin: 0.55rem 0 0;
            color: var(--alab-text-2);
            font-size: 0.96rem;
            line-height: 1.55;
        }

        .alab-dashboard-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 0.95rem;
        }

        .alab-dashboard-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            min-height: 34px;
            padding: 0.35rem 0.72rem;
            border-radius: 999px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            color: var(--alab-text-2);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .alab-dashboard-chip strong {
            color: var(--alab-text-1);
            font-weight: 800;
        }

        .stApp p,
        .stApp li,
        .stApp label,
        .stApp .stMarkdown,
        .stApp .stMarkdown p,
        .stApp .stCaption,
        .stApp [data-testid="stCaptionContainer"],
        .stApp [data-testid="stText"],
        .stApp [data-testid="stMarkdownContainer"] {
            color: var(--alab-text-2);
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6,
        .stApp .stSubheader,
        .stApp .stHeader {
            color: var(--alab-text-1);
        }

        .stApp a,
        .stApp a:visited,
        .stApp .stMarkdown a,
        .stApp .stMarkdown a:visited {
            color: #8fd3b4;
            text-decoration-color: rgba(143, 211, 180, 0.55);
        }

        .stApp a:hover,
        .stApp .stMarkdown a:hover {
            color: #c6f5df;
        }

        .stApp [data-testid="stMetric"] {
            color: var(--alab-text-1);
        }

        .stApp [data-testid="stMetricLabel"] p,
        .stApp [data-testid="stMetricLabel"] div {
            color: var(--alab-text-3);
            font-weight: 700;
            letter-spacing: 0.04em;
        }

        .stApp [data-testid="stMetricValue"] div,
        .stApp [data-testid="stMetricValue"] p {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-weight: 700;
        }

        .stApp [data-testid="stMetricDelta"] div,
        .stApp [data-testid="stMetricDelta"] p {
            color: var(--alab-text-2);
        }

        .stApp hr,
        .stApp [data-testid="stDivider"] {
            border-color: rgba(255, 255, 255, 0.14);
        }

        .stApp [data-testid="stForm"] {
            padding: 1rem 1rem 0.4rem;
            border-radius: var(--alab-radius-lg);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: linear-gradient(145deg, rgba(21, 40, 33, 0.55), rgba(10, 26, 20, 0.42));
        }

        .stApp [data-testid="stExpander"] {
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: var(--alab-radius-md);
            background: rgba(9, 21, 17, 0.38);
            box-shadow: var(--alab-shadow-sm);
            overflow: hidden;
        }

        .stApp [data-testid="stExpander"] summary {
            background: linear-gradient(135deg, rgba(28, 52, 42, 0.92), rgba(12, 26, 20, 0.97));
            color: var(--alab-text-1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }

        .stApp [data-testid="stExpander"] summary:hover {
            background: linear-gradient(135deg, rgba(36, 66, 54, 0.96), rgba(15, 31, 24, 0.98));
        }

        .stApp [data-testid="stExpander"] summary p,
        .stApp [data-testid="stExpander"] summary span,
        .stApp [data-testid="stExpanderToggleIcon"] {
            color: var(--alab-text-1) !important;
            fill: var(--alab-text-1) !important;
        }

        .stApp label[data-testid="stWidgetLabel"] p,
        .stApp .stSelectbox label p,
        .stApp .stTextInput label p,
        .stApp .stTextArea label p,
        .stApp .stDateInput label p,
        .stApp .stNumberInput label p,
        .stApp .stMultiSelect label p {
            color: var(--alab-text-1);
            font-weight: 600;
        }

        .stApp input,
        .stApp textarea,
        .stApp [data-baseweb="input"] input,
        .stApp [data-baseweb="base-input"] input,
        .stApp [data-baseweb="base-input"] textarea {
            color: #f4fbf7 !important;
            -webkit-text-fill-color: #f4fbf7 !important;
            caret-color: #f4fbf7 !important;
        }

        .stApp input::placeholder,
        .stApp textarea::placeholder,
        .stApp [data-baseweb="input"] input::placeholder,
        .stApp [data-baseweb="base-input"] textarea::placeholder {
            color: rgba(226, 236, 231, 0.5) !important;
            -webkit-text-fill-color: rgba(226, 236, 231, 0.5) !important;
        }

        .stApp [data-baseweb="input"],
        .stApp [data-baseweb="base-input"],
        .stApp [data-baseweb="select"] > div,
        .stApp .stDateInput > div,
        .stApp .stNumberInput > div {
            background: rgba(13, 29, 23, 0.88) !important;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .stApp [data-baseweb="select"] * {
            color: #f4fbf7 !important;
        }

        .stApp [data-baseweb="select"] svg,
        .stApp .stDateInput svg {
            fill: rgba(244, 251, 247, 0.88);
        }

        .stApp [data-baseweb="tag"] {
            background: rgba(90, 154, 124, 0.18) !important;
            border: 1px solid rgba(90, 154, 124, 0.34) !important;
        }

        .stApp [data-baseweb="tag"] span,
        .stApp [data-baseweb="tag"] div {
            color: var(--alab-text-1) !important;
        }

        .stApp [data-baseweb="input"]:focus-within,
        .stApp [data-baseweb="base-input"]:focus-within,
        .stApp [data-baseweb="select"] > div:focus-within,
        .stApp .stDateInput > div:focus-within,
        .stApp .stNumberInput > div:focus-within {
            border-color: rgba(143, 211, 180, 0.7) !important;
            box-shadow: 0 0 0 1px rgba(143, 211, 180, 0.34), 0 0 0 4px rgba(143, 211, 180, 0.08);
        }

        .stApp small,
        .stApp .stForm small {
            color: rgba(226, 236, 231, 0.62) !important;
        }

        .stApp .stButton > button,
        .stApp .stFormSubmitButton > button {
            min-height: 42px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.14);
            background: linear-gradient(135deg, rgba(35, 67, 55, 0.96), rgba(10, 26, 20, 0.98));
            color: #f6fcf8;
            font-family: 'Manrope', sans-serif;
            font-size: 0.94rem;
            font-weight: 700;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
            transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease;
        }

        .stApp .stButton > button:hover,
        .stApp .stFormSubmitButton > button:hover {
            border-color: rgba(143, 211, 180, 0.54);
            background: linear-gradient(135deg, rgba(53, 98, 80, 0.98), rgba(14, 31, 24, 0.99));
            color: #ffffff;
            transform: translateY(-1px);
        }

        .stApp .stButton > button[kind="primary"],
        .stApp .stFormSubmitButton > button[kind="primary"] {
            border-color: rgba(143, 211, 180, 0.58);
            background: linear-gradient(135deg, rgba(90, 154, 124, 0.42), rgba(24, 54, 43, 0.98));
            color: #ffffff;
        }

        .stApp .stButton > button:disabled,
        .stApp .stFormSubmitButton > button:disabled,
        .stApp .stButton > button[disabled],
        .stApp .stFormSubmitButton > button[disabled] {
            border-color: rgba(255, 255, 255, 0.09) !important;
            background: linear-gradient(135deg, rgba(44, 55, 50, 0.9), rgba(25, 31, 28, 0.92)) !important;
            color: rgba(236, 244, 240, 0.5) !important;
            opacity: 1 !important;
            box-shadow: none;
            cursor: not-allowed;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10, 20, 17, 0.99), rgba(6, 15, 13, 0.99)) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--alab-text-1);
        }

        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] [data-testid="stText"],
        [data-testid="stSidebar"] label p,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: var(--alab-text-1) !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 42px;
            justify-content: flex-start;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            background: linear-gradient(135deg, rgba(20, 34, 30, 0.96), rgba(8, 18, 15, 0.98));
            color: var(--alab-text-1);
            font-family: 'Manrope', sans-serif;
            font-size: 0.92rem;
            font-weight: 700;
            box-shadow: none;
            transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: rgba(25, 226, 143, 0.34);
            background: linear-gradient(135deg, rgba(28, 50, 43, 0.98), rgba(11, 24, 20, 0.99));
            transform: translateY(-1px);
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            border-color: rgba(25, 226, 143, 0.4);
            background:
                linear-gradient(135deg, rgba(164, 206, 189, 0.32), rgba(38, 77, 64, 0.98) 24%, rgba(10, 22, 18, 0.99));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.12);
        }

        .alab-section-title,
        .panel-title {
            color: var(--alab-brand);
            font-family: 'Sora', sans-serif;
            font-weight: 700;
            font-size: 0.98rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 0.2rem 0 0.6rem;
            text-align: center;
        }

        .alab-block-header {
            margin: 0.25rem 0 1rem;
            padding: 0.15rem 0 0.6rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }

        .alab-block-header-center {
            text-align: center;
        }

        .alab-block-eyebrow {
            color: var(--alab-brand);
            font-size: 0.7rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.32rem;
        }

        .alab-block-title {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.08rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .alab-block-copy {
            max-width: 720px;
            margin-top: 0.35rem;
            color: var(--alab-text-3);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .alab-inline-note {
            margin: 0.15rem 0 0.9rem;
            padding: 0.72rem 0.85rem;
            border-radius: var(--alab-radius-sm);
            border: 1px solid rgba(255, 255, 255, 0.06);
            background: rgba(255, 255, 255, 0.03);
            color: var(--alab-text-3);
            font-size: 0.84rem;
            line-height: 1.5;
        }

        .alab-mini-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 0.8rem;
            margin: 0.25rem 0 1rem;
        }

        .alab-mini-stat {
            padding: 0.85rem 0.95rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background:
                linear-gradient(90deg, rgba(25, 226, 143, 0.08), transparent 38%),
                linear-gradient(145deg, rgba(17, 28, 25, 0.98), rgba(8, 19, 16, 0.98));
            box-shadow: var(--alab-shadow-sm);
        }

        .alab-mini-label {
            display: block;
            color: var(--alab-text-3);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .alab-mini-value {
            display: block;
            margin-top: 0.4rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.2rem;
            font-weight: 800;
            line-height: 1.05;
        }

        .alab-mini-copy {
            display: block;
            margin-top: 0.22rem;
            color: var(--alab-text-3);
            font-size: 0.76rem;
            line-height: 1.45;
        }

        .alab-kpi-grid,
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.6rem;
        }

        .alab-kpi,
        .kpi-card {
            position: relative;
            overflow: hidden;
            padding: 1.1rem 1.15rem 1rem;
            border-radius: var(--alab-radius-lg);
            border: 1px solid rgba(255, 255, 255, 0.09);
            background:
                radial-gradient(circle at top right, rgba(25, 226, 143, 0.1), transparent 30%),
                linear-gradient(145deg, rgba(19, 30, 27, 0.98), rgba(8, 19, 16, 0.98));
            box-shadow: var(--alab-shadow-md);
        }

        .alab-kpi::before,
        .kpi-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 72px;
            height: 2px;
            background: linear-gradient(90deg, rgba(25, 226, 143, 0.92), rgba(25, 226, 143, 0));
        }

        .alab-kpi-label,
        .kpi-title,
        .card-title {
            color: var(--alab-text-3);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .alab-kpi-value,
        .kpi-value,
        .card-value {
            margin-top: 0.5rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 2.1rem;
            font-weight: 800;
            line-height: 1.05;
        }

        .alab-rank-card,
        .rank-card {
            position: relative;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 0.55rem;
            padding: 0.92rem 1rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background:
                linear-gradient(90deg, rgba(25, 226, 143, 0.08), transparent 36%),
                linear-gradient(140deg, rgba(18, 30, 27, 0.98), rgba(8, 19, 16, 0.96));
            box-shadow: var(--alab-shadow-sm);
        }

        .alab-rank-left,
        .rank-left {
            display: flex;
            gap: 0.8rem;
            align-items: center;
        }

        .alab-rank-num,
        .rank-num {
            width: 34px;
            color: var(--alab-warning);
            font-family: 'Sora', sans-serif;
            font-weight: 800;
            text-align: center;
        }

        .alab-rank-name,
        .rank-name {
            color: var(--alab-text-1);
            font-size: 0.92rem;
            font-weight: 700;
        }

        .alab-rank-score,
        .rank-score {
            color: #9ef0c7;
            font-family: 'Sora', sans-serif;
            font-weight: 800;
            font-size: 1.04rem;
        }

        .alab-player-panel {
            padding: 1rem 1rem 0.95rem;
            border-radius: var(--alab-radius-lg);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background:
                linear-gradient(180deg, rgba(30, 60, 114, 0.1), transparent 46%),
                linear-gradient(150deg, rgba(27, 51, 42, 0.92), rgba(10, 26, 20, 0.97));
            box-shadow: var(--alab-shadow-md);
        }

        .alab-player-panel-title {
            margin: 0 0 0.65rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.15;
        }

        .alab-player-panel-copy {
            color: var(--alab-text-2);
            font-size: 0.9rem;
            line-height: 1.58;
        }

        .alab-player-panel-copy strong {
            color: var(--alab-text-1);
        }

        .alab-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-bottom: 0.9rem;
        }

        .alab-badge,
        .label {
            display: inline-flex;
            align-items: center;
            min-height: 24px;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .alab-badge-muted {
            background: rgba(255, 255, 255, 0.04);
            color: var(--alab-text-2);
        }

        .alab-detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 0.7rem;
        }

        .alab-detail-item {
            padding: 0.72rem 0.78rem;
            border-radius: var(--alab-radius-sm);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .alab-detail-label {
            display: block;
            margin-bottom: 0.22rem;
            color: var(--alab-text-3);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .alab-detail-value {
            color: var(--alab-text-1);
            font-size: 0.92rem;
            font-weight: 600;
            line-height: 1.35;
        }

        .alab-player-card,
        .player-card {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            width: 100%;
            min-height: 82px;
            margin: 0.35rem auto;
            padding: 0.85rem 0.95rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid rgba(255, 255, 255, 0.07);
            background: linear-gradient(130deg, rgba(58, 102, 81, 0.88), rgba(10, 26, 20, 0.95));
            box-shadow: var(--alab-shadow-sm);
        }

        .alab-player-photo,
        .player-photo {
            width: 56px;
            height: 56px;
            border-radius: 16px;
            object-fit: cover;
            border: 1px solid rgba(90, 154, 124, 0.55);
        }

        .alab-player-name,
        .player-info h5 {
            margin: 0 0 0.16rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 0.88rem;
            font-weight: 700;
        }

        .alab-player-copy,
        .player-info p {
            margin: 0.08rem 0;
            color: var(--alab-text-3);
            font-size: 0.77rem;
            line-height: 1.35;
        }

        .alab-player-link a,
        .player-link a {
            color: var(--alab-brand);
            font-size: 0.74rem;
            font-weight: 700;
            text-decoration: none;
        }

        .alab-line-title,
        .line-title {
            color: var(--alab-brand);
            font-family: 'Sora', sans-serif;
            font-weight: 700;
            font-size: 0.94rem;
            letter-spacing: 0.03em;
            margin: 0.1rem 0 0.6rem;
            text-align: center;
        }

        .alab-panel-title,
        .panel-title {
            margin: 0.2rem 0 0.75rem;
            padding: 0.75rem 0.85rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: linear-gradient(145deg, rgba(18, 30, 27, 0.96), rgba(8, 19, 16, 0.98));
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 0.92rem;
            font-weight: 700;
            text-align: center;
            box-shadow: var(--alab-shadow-sm);
        }

        .alab-empty-slot {
            color: var(--alab-text-3);
            font-size: 0.76rem;
            text-align: center;
            padding: 0.5rem 0 0.35rem;
        }

        .alab-card,
        .card {
            width: 100%;
            min-height: 146px;
            padding: 0.95rem 1rem;
            border-radius: var(--alab-radius-lg);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background:
                linear-gradient(180deg, rgba(30, 60, 114, 0.12), transparent 44%),
                linear-gradient(140deg, rgba(58, 102, 81, 0.9), rgba(10, 26, 20, 0.96));
            box-shadow: var(--alab-shadow-md);
            color: var(--alab-text-1);
        }

        .alab-card h5,
        .card h5 {
            margin: 0.2rem 0 0.35rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 0.94rem;
        }

        .alab-card p,
        .card p {
            margin: 0.16rem 0;
            color: var(--alab-text-2);
            font-size: 0.81rem;
            line-height: 1.45;
        }

        .alab-card-seen,
        .card.visto {
            opacity: 0.84;
            background: linear-gradient(130deg, rgba(26, 31, 46, 0.92), rgba(42, 58, 90, 0.86));
        }

        .alab-badge-vencido,
        .vencido {
            background-color: rgba(139, 0, 0, 0.88);
            color: #ffffff;
        }

        .alab-badge-hoy,
        .hoy {
            background-color: rgba(255, 215, 0, 0.94);
            color: #000000;
        }

        .alab-badge-proximo,
        .proximo {
            background-color: rgba(0, 100, 0, 0.9);
            color: #ffffff;
        }

        .alab-badge-futuro,
        .futuro {
            background-color: rgba(0, 68, 136, 0.88);
            color: #ffffff;
        }

        @media (max-width: 1024px) {
            .alab-kpi-grid,
            .kpi-container,
            .alab-mini-grid {
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            }

            .alab-dashboard-hero {
                padding: 1.2rem 1.1rem 1.1rem;
                border-radius: 22px;
            }

            .alab-detail-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )