import streamlit as st


def load_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

        :root {
            --alab-bg-0: #090b0f;
            --alab-bg-1: #0d1015;
            --alab-bg-2: #12161c;
            --alab-bg-3: #171b22;
            --alab-surface-1: #12161c;
            --alab-surface-2: #171b22;
            --alab-surface-3: #1c212a;
            --alab-surface-4: #212733;
            --alab-sidebar: #0d0f14;
            --alab-brand: #25b86a;
            --alab-brand-hover: #2dcc78;
            --alab-brand-soft: rgba(37, 184, 106, 0.12);
            --alab-brand-line: rgba(37, 184, 106, 0.32);
            --alab-text-1: #f4f6f8;
            --alab-text-2: #a7afba;
            --alab-text-3: #77808d;
            --alab-text-4: #636c78;
            --alab-border: rgba(255, 255, 255, 0.08);
            --alab-border-strong: rgba(255, 255, 255, 0.13);
            --alab-info: #4ea1ff;
            --alab-warning: #e4b64c;
            --alab-danger: #ef6262;
            --alab-radius-lg: 16px;
            --alab-radius-md: 12px;
            --alab-radius-sm: 8px;
            --alab-shadow-lg: 0 22px 54px rgba(0, 0, 0, 0.24);
            --alab-shadow-md: 0 12px 28px rgba(0, 0, 0, 0.18);
            --alab-shadow-sm: 0 6px 18px rgba(0, 0, 0, 0.14);
        }

        html,
        body,
        .stApp,
        .stApp button,
        .stApp input,
        .stApp select,
        .stApp textarea {
            font-family: 'Manrope', 'Inter', system-ui, sans-serif;
        }

        html,
        body,
        .stApp,
        .stApp [data-baseweb="input"],
        .stApp [data-baseweb="base-input"],
        .stApp [data-baseweb="select"] > div,
        .stApp input,
        .stApp select,
        .stApp textarea {
            color-scheme: dark;
        }

        .stApp {
            position: relative;
            min-height: 100vh;
            background:
                radial-gradient(circle at top left, rgba(37, 184, 106, 0.05), transparent 22%),
                radial-gradient(circle at bottom right, rgba(78, 161, 255, 0.04), transparent 20%),
                linear-gradient(180deg, #090b0f 0%, #0b0d11 36%, #0b0e12 100%);
            background-attachment: fixed;
            color: var(--alab-text-1);
        }

        .stApp::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.015), rgba(255, 255, 255, 0) 34%),
                radial-gradient(circle at 18% 10%, rgba(255, 255, 255, 0.02), transparent 14%),
                radial-gradient(circle at 84% 8%, rgba(37, 184, 106, 0.04), transparent 14%);
            opacity: 1;
            z-index: 0;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                radial-gradient(circle at 24% 22%, rgba(255, 255, 255, 0.025), transparent 1px),
                radial-gradient(circle at 72% 34%, rgba(255, 255, 255, 0.02), transparent 1px);
            background-size: 22px 22px, 26px 26px;
            opacity: 0.22;
            z-index: 0;
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: transparent;
            position: relative;
            z-index: 1;
        }

        [data-testid="stHeader"] {
            background: rgba(9, 11, 15, 0.92);
            border-bottom: 1px solid var(--alab-border);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
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
            background: linear-gradient(90deg, rgba(37, 184, 106, 0.8), rgba(37, 184, 106, 0.12));
            height: 2px;
        }

        [data-testid="stAppViewContainer"] .block-container {
            max-width: 1380px;
            padding-top: 1.5rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 1.25rem;
        }

        .alab-dashboard-hero {
            position: relative;
            overflow: hidden;
            margin: 0.25rem 0 1.1rem;
            padding: 0.35rem 0 0.1rem;
            border: 0;
            border-radius: 0;
            background: transparent;
            box-shadow: none;
        }

        .alab-dashboard-hero::before {
            content: "";
            position: absolute;
            inset: auto auto 0 0;
            width: 72px;
            height: 2px;
            background: linear-gradient(90deg, rgba(37, 184, 106, 0.85), rgba(37, 184, 106, 0));
        }

        .alab-dashboard-hero-kicker {
            color: var(--alab-brand);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.38rem;
        }

        .alab-dashboard-hero-title {
            margin: 0;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: clamp(2rem, 3vw, 2.45rem);
            font-weight: 700;
            line-height: 1.05;
        }

        .alab-dashboard-hero-copy {
            max-width: 780px;
            margin: 0.45rem 0 0;
            color: var(--alab-text-2);
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .alab-dashboard-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.8rem;
        }

        .alab-dashboard-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            min-height: 30px;
            padding: 0.28rem 0.68rem;
            border-radius: 999px;
            border: 1px solid var(--alab-border);
            background: rgba(255, 255, 255, 0.02);
            color: var(--alab-text-2);
            font-size: 0.72rem;
            font-weight: 600;
        }

        .alab-dashboard-chip strong {
            color: var(--alab-text-1);
            font-weight: 700;
        }

        .alab-login-hero {
            position: relative;
            overflow: hidden;
            margin: 0 auto 1.4rem;
            padding: 1.45rem 1.5rem 1.35rem;
            max-width: 1180px;
            border-radius: var(--alab-radius-lg);
            border: 1px solid var(--alab-border);
            background:
                radial-gradient(circle at top right, rgba(37, 184, 106, 0.08), transparent 24%),
                linear-gradient(180deg, rgba(18, 22, 28, 0.96), rgba(13, 16, 21, 0.98));
            box-shadow: var(--alab-shadow-md);
        }

        .alab-login-top-spacer {
            height: 1.4rem;
        }

        .alab-login-section-gap {
            height: 0.35rem;
        }

        .alab-login-hero::before {
            content: "";
            position: absolute;
            inset: 0 auto auto 0;
            width: 88px;
            height: 2px;
            background: linear-gradient(90deg, rgba(37, 184, 106, 0.92), rgba(37, 184, 106, 0));
        }

        .alab-login-kicker {
            color: var(--alab-brand);
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            margin-bottom: 0.38rem;
        }

        .alab-login-title {
            margin: 0;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: clamp(2rem, 3vw, 2.8rem);
            font-weight: 700;
            line-height: 1.06;
        }

        .alab-login-copy {
            max-width: 760px;
            margin: 0.55rem 0 0;
            color: var(--alab-text-2);
            font-size: 0.96rem;
            line-height: 1.55;
        }

        .alab-login-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }

        .alab-login-sidecard {
            min-height: 100%;
            padding: 1.2rem 1.15rem 1.1rem;
            border-radius: var(--alab-radius-lg);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(18, 22, 28, 0.95), rgba(14, 18, 24, 0.98));
            box-shadow: var(--alab-shadow-sm);
        }

        .alab-login-sidecard-title {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.02rem;
            font-weight: 700;
            line-height: 1.18;
        }

        .alab-login-sidecard-copy {
            margin: 0.55rem 0 0;
            color: var(--alab-text-2);
            font-size: 0.9rem;
            line-height: 1.56;
        }

        .alab-login-bullet-list {
            display: flex;
            flex-direction: column;
            gap: 0.64rem;
            margin-top: 1rem;
        }

        .alab-login-bullet {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--alab-text-1);
            font-size: 0.82rem;
            font-weight: 600;
        }

        .alab-login-bullet::before {
            content: "";
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: var(--alab-brand);
            box-shadow: 0 0 0 5px rgba(37, 184, 106, 0.1);
            flex: 0 0 auto;
        }

        .alab-login-form-head {
            margin: 0 0 0.85rem;
            padding: 0.15rem 0.1rem;
        }

        .alab-login-form-title {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .alab-login-form-copy {
            margin: 0.38rem 0 0;
            color: var(--alab-text-2);
            font-size: 0.88rem;
            line-height: 1.5;
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

        .stApp [data-testid="stMarkdownContainer"] p {
            line-height: 1.5;
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
            font-family: 'Sora', 'Manrope', sans-serif;
        }

        .stApp a,
        .stApp a:visited,
        .stApp .stMarkdown a,
        .stApp .stMarkdown a:visited {
            color: #8adcae;
            text-decoration-color: rgba(138, 220, 174, 0.45);
        }

        .stApp a:hover,
        .stApp .stMarkdown a:hover {
            color: #d9f7e6;
        }

        .stApp [data-testid="stMetric"] {
            color: var(--alab-text-1);
        }

        .stApp [data-testid="stMetricLabel"] p,
        .stApp [data-testid="stMetricLabel"] div {
            color: var(--alab-text-3);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
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
            border-color: var(--alab-border);
        }

        .stApp [data-testid="stForm"] {
            padding: 0.95rem 1rem 0.3rem;
            border-radius: var(--alab-radius-lg);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.92), rgba(17, 21, 27, 0.98));
            box-shadow: var(--alab-shadow-sm);
        }

        .stApp [data-testid="stExpander"] {
            border: 1px solid var(--alab-border);
            border-radius: var(--alab-radius-md);
            background: rgba(18, 22, 29, 0.92);
            box-shadow: none;
            overflow: hidden;
        }

        .stApp [data-testid="stExpander"] summary {
            background: rgba(20, 24, 31, 0.96);
            color: var(--alab-text-1);
            border-bottom: 1px solid var(--alab-border);
        }

        .stApp [data-testid="stExpander"] summary:hover {
            background: rgba(24, 29, 37, 0.98);
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
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 0.24rem;
        }

        .stApp input,
        .stApp textarea,
        .stApp [data-baseweb="input"] input,
        .stApp [data-baseweb="base-input"] input,
        .stApp [data-baseweb="base-input"] textarea {
            color: var(--alab-text-1) !important;
            -webkit-text-fill-color: var(--alab-text-1) !important;
            caret-color: var(--alab-text-1) !important;
            background: var(--alab-surface-2) !important;
            background-color: var(--alab-surface-2) !important;
            font-size: 0.9rem !important;
        }

        .stApp input:-webkit-autofill,
        .stApp input:-webkit-autofill:hover,
        .stApp input:-webkit-autofill:focus,
        .stApp textarea:-webkit-autofill,
        .stApp textarea:-webkit-autofill:hover,
        .stApp textarea:-webkit-autofill:focus,
        .stApp [data-baseweb="input"] input:-webkit-autofill,
        .stApp [data-baseweb="input"] input:-webkit-autofill:hover,
        .stApp [data-baseweb="input"] input:-webkit-autofill:focus,
        .stApp [data-baseweb="base-input"] input:-webkit-autofill,
        .stApp [data-baseweb="base-input"] input:-webkit-autofill:hover,
        .stApp [data-baseweb="base-input"] input:-webkit-autofill:focus {
            -webkit-text-fill-color: var(--alab-text-1) !important;
            caret-color: var(--alab-text-1) !important;
            box-shadow: 0 0 0 1000px var(--alab-surface-2) inset !important;
            -webkit-box-shadow: 0 0 0 1000px var(--alab-surface-2) inset !important;
            transition: background-color 9999s ease-out 0s !important;
        }

        .stApp [data-baseweb="select"] > div,
        .stApp [data-baseweb="select"] input,
        .stApp [data-baseweb="select"] div,
        .stApp [data-baseweb="select"] span,
        .stApp .stDateInput [data-baseweb="input"] * ,
        .stApp .stNumberInput [data-baseweb="input"] * {
            color: var(--alab-text-1) !important;
            -webkit-text-fill-color: var(--alab-text-1) !important;
        }

        .stApp input::placeholder,
        .stApp textarea::placeholder,
        .stApp [data-baseweb="input"] input::placeholder,
        .stApp [data-baseweb="base-input"] textarea::placeholder,
        .stApp [data-baseweb="select"] input::placeholder {
            color: rgba(167, 175, 186, 0.68) !important;
            -webkit-text-fill-color: rgba(167, 175, 186, 0.68) !important;
        }

        .stApp [data-baseweb="input"],
        .stApp [data-baseweb="base-input"],
        .stApp [data-baseweb="select"] > div,
        .stApp .stDateInput > div,
        .stApp .stNumberInput > div {
            min-height: 40px;
            background: var(--alab-surface-2) !important;
            border-radius: var(--alab-radius-sm);
            border: 1px solid rgba(43, 48, 57, 1) !important;
            box-shadow: none !important;
        }

        .stApp [data-baseweb="input"] > div,
        .stApp [data-baseweb="base-input"] > div,
        .stApp .stDateInput [data-baseweb="input"] > div,
        .stApp .stNumberInput [data-baseweb="input"] > div {
            background: var(--alab-surface-2) !important;
            background-color: var(--alab-surface-2) !important;
        }

        .stApp [data-baseweb="select"] * {
            color: var(--alab-text-1) !important;
        }

        .stApp [data-baseweb="popover"],
        .stApp [role="listbox"],
        .stApp [role="option"] {
            color: var(--alab-text-1) !important;
        }

        .stApp [role="listbox"] {
            background: var(--alab-surface-2) !important;
            border: 1px solid rgba(43, 48, 57, 1) !important;
        }

        .stApp [role="option"] {
            background: transparent !important;
        }

        .stApp [role="option"][aria-selected="true"],
        .stApp [role="option"]:hover {
            background: rgba(255, 255, 255, 0.06) !important;
        }

        .stApp [data-baseweb="select"] svg,
        .stApp .stDateInput svg {
            fill: rgba(244, 246, 248, 0.78);
        }

        .stApp [data-baseweb="tag"] {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid var(--alab-border) !important;
            border-radius: 999px !important;
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
            border-color: rgba(37, 184, 106, 0.82) !important;
            box-shadow: 0 0 0 1px rgba(37, 184, 106, 0.28), 0 0 0 3px rgba(37, 184, 106, 0.07) !important;
        }

        .stApp small,
        .stApp .stForm small {
            color: rgba(167, 175, 186, 0.72) !important;
        }

        .stApp .stButton > button,
        .stApp .stFormSubmitButton > button {
            min-height: 38px;
            border-radius: var(--alab-radius-sm);
            border: 1px solid var(--alab-border-strong);
            background: var(--alab-surface-2);
            color: var(--alab-text-1);
            font-family: 'Manrope', sans-serif;
            font-size: 0.86rem;
            font-weight: 700;
            box-shadow: none;
            transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease, color 0.18s ease;
        }

        .stApp .stButton > button:hover,
        .stApp .stFormSubmitButton > button:hover {
            border-color: rgba(255, 255, 255, 0.18);
            background: var(--alab-surface-3);
            color: #ffffff;
            transform: translateY(-1px);
        }

        .stApp .stButton > button[kind="primary"],
        .stApp .stFormSubmitButton > button[kind="primary"] {
            border-color: rgba(37, 184, 106, 0.4);
            background: linear-gradient(180deg, rgba(43, 196, 116, 0.98), rgba(31, 158, 92, 0.98));
            color: #08100b;
            box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.12);
        }

        .stApp .stButton > button[kind="primary"]:hover,
        .stApp .stFormSubmitButton > button[kind="primary"]:hover {
            border-color: rgba(45, 204, 120, 0.48);
            background: linear-gradient(180deg, rgba(55, 205, 125, 1), rgba(36, 171, 103, 1));
            color: #051009;
        }

        .stApp .stButton > button:disabled,
        .stApp .stFormSubmitButton > button:disabled,
        .stApp .stButton > button[disabled],
        .stApp .stFormSubmitButton > button[disabled] {
            border-color: rgba(255, 255, 255, 0.06) !important;
            background: rgba(27, 31, 38, 0.92) !important;
            color: rgba(167, 175, 186, 0.45) !important;
            opacity: 1 !important;
            box-shadow: none;
            cursor: not-allowed;
        }

        [data-testid="stSidebar"] {
            min-width: 236px;
            max-width: 245px;
            background: linear-gradient(180deg, rgba(13, 15, 20, 0.99), rgba(10, 12, 17, 0.99)) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.07);
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
        }

        [data-testid="stSidebarNav"] {
            display: none;
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

        [data-testid="stSidebar"] .block-container,
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
            gap: 0.35rem;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            min-height: 36px;
            justify-content: flex-start;
            padding: 0.4rem 0.8rem;
            border-radius: 10px;
            border: 1px solid transparent;
            background: transparent;
            color: var(--alab-text-2);
            font-family: 'Manrope', sans-serif;
            font-size: 0.84rem;
            font-weight: 600;
            box-shadow: none;
            transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease, color 0.18s ease;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            border-color: rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.04);
            color: var(--alab-text-1);
            transform: none;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            border-color: rgba(255, 255, 255, 0.08);
            background: rgba(255, 255, 255, 0.06);
            color: var(--alab-text-1);
            box-shadow: inset 3px 0 0 var(--alab-brand);
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            border-color: rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.075);
            color: #ffffff;
        }

        .alab-sidebar-title {
            margin: 0 0 0.25rem;
            color: var(--alab-text-3);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .alab-sidebar-user {
            margin: 0.15rem 0 0.6rem;
            padding: 0.9rem 0.95rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(15, 18, 24, 0.98));
        }

        .alab-sidebar-user-label {
            display: block;
            color: var(--alab-text-4);
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.22rem;
        }

        .alab-sidebar-user-value {
            display: block;
            color: var(--alab-text-1);
            font-size: 0.84rem;
            font-weight: 700;
            line-height: 1.35;
        }

        .alab-sidebar-user + .stButton > button {
            margin-top: 0.05rem;
        }

        .alab-sidebar-nav-spacer {
            height: 0.3rem;
        }

        .alab-section-title,
        .panel-title {
            color: var(--alab-brand);
            font-family: 'Sora', sans-serif;
            font-weight: 700;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin: 0.15rem 0 0.45rem;
            text-align: left;
        }

        .alab-block-header {
            margin: 0.2rem 0 0.9rem;
            padding: 0.15rem 0 0.55rem;
            border-bottom: 1px solid var(--alab-border);
        }

        .alab-block-header-center {
            text-align: center;
        }

        .alab-block-eyebrow {
            color: var(--alab-brand);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.26rem;
        }

        .alab-block-title {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .alab-block-copy {
            max-width: 720px;
            margin-top: 0.28rem;
            color: var(--alab-text-3);
            font-size: 0.85rem;
            line-height: 1.5;
        }

        .alab-inline-note {
            margin: 0.15rem 0 0.9rem;
            padding: 0.7rem 0.82rem;
            border-radius: var(--alab-radius-sm);
            border: 1px solid var(--alab-border);
            background: rgba(255, 255, 255, 0.02);
            color: var(--alab-text-3);
            font-size: 0.8rem;
            line-height: 1.5;
        }

        .alab-mini-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 0.75rem;
            margin: 0.2rem 0 1rem;
        }

        .alab-mini-stat {
            padding: 0.95rem 1rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(17, 21, 27, 0.98));
            box-shadow: none;
        }

        .alab-mini-label {
            display: block;
            color: var(--alab-text-3);
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .alab-mini-value {
            display: block;
            margin-top: 0.48rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1;
        }

        .alab-mini-copy {
            display: block;
            margin-top: 0.3rem;
            color: var(--alab-text-3);
            font-size: 0.76rem;
            line-height: 1.45;
        }

        .alab-kpi-grid,
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 0.85rem;
            margin: 0.9rem 0 1.3rem;
        }

        .alab-kpi,
        .kpi-card {
            position: relative;
            overflow: hidden;
            padding: 1rem 1.05rem 0.95rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(17, 21, 27, 0.98));
            box-shadow: none;
        }

        .alab-kpi::before,
        .kpi-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 56px;
            height: 2px;
            background: linear-gradient(90deg, rgba(37, 184, 106, 0.82), rgba(37, 184, 106, 0));
        }

        .alab-kpi-label,
        .kpi-title,
        .card-title {
            color: var(--alab-text-3);
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .alab-kpi-value,
        .kpi-value,
        .card-value {
            margin-top: 0.52rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: clamp(1.8rem, 2vw, 2.15rem);
            font-weight: 700;
            line-height: 1.02;
        }

        .alab-rank-card,
        .rank-card {
            position: relative;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.45rem;
            padding: 0.78rem 0.86rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(17, 21, 27, 0.98));
            box-shadow: none;
        }

        .alab-rank-left,
        .rank-left {
            display: flex;
            gap: 0.7rem;
            align-items: center;
            min-width: 0;
        }

        .alab-rank-num,
        .rank-num {
            width: 28px;
            color: var(--alab-warning);
            font-family: 'Sora', sans-serif;
            font-weight: 700;
            text-align: center;
            font-size: 0.88rem;
            line-height: 1;
        }

        .alab-rank-name,
        .rank-name {
            color: var(--alab-text-1);
            font-size: 0.84rem;
            font-weight: 700;
            line-height: 1.25;
        }

        .alab-rank-score,
        .rank-score {
            color: #8ce0af;
            font-family: 'Sora', sans-serif;
            font-weight: 700;
            font-size: 0.92rem;
            line-height: 1;
            white-space: nowrap;
        }

        .alab-top-rank-group {
            margin-bottom: 0.8rem;
        }

        .alab-panel-title.alab-top-rank-title,
        .panel-title.alab-top-rank-title {
            margin: 0 0 0.55rem;
            padding: 0.68rem 0.8rem;
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .alab-rank-card.alab-rank-card-compact,
        .rank-card.alab-rank-card-compact {
            min-height: 0;
            padding: 0.72rem 0.78rem;
            border-radius: 10px;
        }

        .alab-rank-card-compact .alab-rank-name,
        .alab-rank-card-compact .rank-name {
            font-size: 0.8rem;
        }

        .alab-rank-card-compact .alab-rank-score,
        .alab-rank-card-compact .rank-score {
            font-size: 0.9rem;
        }

        .alab-player-panel {
            padding: 1rem 1rem 0.95rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(17, 21, 27, 0.98));
            box-shadow: none;
        }

        .alab-player-panel-tall {
            min-height: 208px;
        }

        .alab-player-media-panel {
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: left;
            padding-top: 1.1rem;
            padding-bottom: 1.1rem;
        }

        .alab-player-media-row {
            display: flex;
            align-items: center;
            gap: 1.1rem;
            width: fit-content;
            max-width: 100%;
            margin: 0 auto;
            min-height: 162px;
        }

        .alab-player-summary {
            display: flex;
            flex: 0 1 340px;
            min-width: 0;
            min-height: auto;
            flex-direction: column;
            justify-content: center;
            gap: 0.55rem;
        }

        .alab-player-summary-focused {
            padding-left: 0.15rem;
        }

        .alab-player-identity-block {
            display: flex;
            flex-direction: column;
            gap: 0.24rem;
        }

        .alab-player-identity-block-compact {
            gap: 0.1rem;
        }

        .alab-player-name {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.22rem;
            font-weight: 700;
            line-height: 1.08;
        }

        .alab-player-subtitle {
            color: var(--alab-text-2);
            font-size: 0.98rem;
            font-weight: 600;
            line-height: 1.26;
        }

        .alab-player-context {
            color: var(--alab-text-3);
            font-size: 0.82rem;
            font-weight: 500;
            line-height: 1.28;
        }

        .alab-player-meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
        }

        .alab-player-meta-pill {
            display: inline-flex;
            align-items: center;
            min-height: 26px;
            padding: 0.24rem 0.58rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--alab-border);
            color: var(--alab-text-2);
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .alab-player-media-wrap {
            display: flex;
            justify-content: flex-start;
            flex: 0 0 auto;
            margin: 0;
        }

        .alab-player-photo {
            width: 168px;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border-radius: 12px;
            border: 1px solid var(--alab-border);
            box-shadow: none;
            background: rgba(255, 255, 255, 0.02);
        }

        .alab-player-photo-placeholder {
            display: grid;
            place-items: center;
            width: 168px;
            aspect-ratio: 1 / 1;
            border-radius: 12px;
            border: 1px solid var(--alab-border);
            background: rgba(255, 255, 255, 0.02);
            color: var(--alab-text-3);
            font-size: 0.84rem;
            font-weight: 700;
        }

        .alab-player-link-row {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.5rem;
            margin-top: auto;
        }

        .alab-player-link-row-inline {
            flex: 0 1 auto;
            justify-content: flex-start;
            align-content: center;
            margin-top: 0;
            row-gap: 0.5rem;
            column-gap: 0.6rem;
        }

        .alab-player-link {
            display: inline-flex;
            align-items: center;
            min-height: 34px;
            padding: 0.38rem 0.78rem;
            border-radius: 999px;
            border: 1px solid var(--alab-border);
            background: rgba(255, 255, 255, 0.02);
            font-size: 0.78rem;
            font-weight: 600;
        }

        .alab-player-link-disabled {
            color: var(--alab-text-3);
            background: rgba(255, 255, 255, 0.025);
        }

        .alab-player-link a,
        .alab-player-link a:visited {
            color: var(--alab-text-2);
            text-decoration: none;
        }

        .alab-player-link a:hover {
            color: var(--alab-text-1);
        }

        .alab-player-cta-gap {
            height: 1.15rem;
        }

        .alab-player-panel-title {
            margin: 0 0 0.65rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            line-height: 1.18;
        }

        .alab-player-panel-copy {
            color: var(--alab-text-2);
            font-size: 0.85rem;
            line-height: 1.56;
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
            padding: 0.22rem 0.56rem;
            border-radius: 999px;
            font-size: 0.64rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            border: 1px solid var(--alab-border);
        }

        .alab-badge-muted {
            background: rgba(255, 255, 255, 0.03);
            color: var(--alab-text-2);
        }

        .alab-detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 0.72rem;
        }

        .alab-detail-item {
            padding: 0.8rem 0.82rem;
            border-radius: var(--alab-radius-sm);
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid var(--alab-border);
        }

        .alab-detail-label {
            display: block;
            margin-bottom: 0.22rem;
            color: var(--alab-text-3);
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .alab-detail-value {
            color: var(--alab-text-1);
            font-size: 0.88rem;
            font-weight: 600;
            line-height: 1.35;
        }

        .alab-compare-card {
            min-height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.85rem;
            padding-bottom: 1.05rem;
            text-align: center;
        }

        .alab-compare-card-empty {
            justify-content: center;
        }

        .alab-compare-kicker {
            color: var(--alab-brand);
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .alab-compare-name {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 1.08rem;
            font-weight: 700;
            line-height: 1.18;
            text-align: center;
        }

        .alab-shortlist-card {
            text-align: left;
        }

        .alab-shortlist-card .alab-compare-name {
            text-align: left;
        }

        .alab-shortlist-body {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            text-align: left;
            width: 100%;
        }

        .alab-shortlist-meta {
            margin: 0;
            color: var(--alab-text-3);
            font-size: 0.94rem;
            line-height: 1.45;
            text-align: left;
        }

        .alab-shortlist-links {
            justify-content: flex-start;
            align-items: center;
            text-align: left;
            width: 100%;
        }

        .alab-shortlist-content {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: nowrap;
            width: 100%;
        }

        .alab-shortlist-copy {
            flex: 1 1 auto;
            min-width: 0;
        }

        .alab-shortlist-rail {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            justify-content: flex-start;
            gap: 0.5rem;
            flex: 0 0 auto;
            min-width: max-content;
            margin-left: auto;
            text-align: right;
        }

        .alab-shortlist-rail .alab-player-link-row {
            justify-content: flex-end;
            width: auto;
        }

        .alab-shortlist-rail .alab-player-link {
            justify-content: flex-end;
        }

        .alab-compare-photo-wrap {
            display: flex;
            justify-content: center;
        }

        .alab-compare-photo,
        .alab-compare-photo-placeholder {
            width: min(100%, 168px);
        }

        .alab-compare-stack {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.55rem;
            width: 100%;
        }

        .alab-compare-card .alab-detail-item,
        .alab-compare-card .alab-detail-label,
        .alab-compare-card .alab-detail-value {
            text-align: center;
        }

        .alab-compare-description {
            margin-top: auto;
            padding: 0.82rem 0.88rem;
            border-radius: var(--alab-radius-sm);
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid var(--alab-border);
            color: var(--alab-text-2);
            font-size: 0.84rem;
            line-height: 1.58;
            text-align: center;
        }

        .alab-compare-empty {
            padding: 1rem 0.95rem;
            border-radius: var(--alab-radius-sm);
            background: rgba(255, 255, 255, 0.025);
            border: 1px dashed rgba(255, 255, 255, 0.14);
            color: var(--alab-text-2);
            font-size: 0.9rem;
            line-height: 1.5;
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
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(17, 21, 27, 0.98));
            box-shadow: none;
        }

        .alab-player-card .alab-player-photo,
        .player-photo {
            width: 56px;
            height: 56px;
            border-radius: 10px;
            object-fit: cover;
            border: 1px solid var(--alab-border);
        }

        .alab-player-card .alab-player-name,
        .player-info h5 {
            margin: 0 0 0.16rem;
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 0.88rem;
            font-weight: 700;
        }

        .alab-player-card .alab-player-copy,
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
            font-weight: 600;
            text-decoration: none;
        }

        .alab-line-title,
        .line-title {
            color: var(--alab-brand);
            font-family: 'Sora', sans-serif;
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 0.08em;
            margin: 0.08rem 0 0.45rem;
            text-align: left;
        }

        .alab-panel-title,
        .panel-title {
            margin: 0.2rem 0 0.75rem;
            padding: 0.7rem 0.82rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(17, 21, 27, 0.98));
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 0.86rem;
            font-weight: 700;
            text-align: left;
            box-shadow: none;
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
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(20, 24, 31, 0.98), rgba(17, 21, 27, 0.98));
            box-shadow: none;
            color: var(--alab-text-1);
        }

        .alab-card h5,
        .card h5 {
            background: linear-gradient(180deg, rgba(23, 27, 34, 0.98), rgba(19, 23, 29, 0.98));
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 0.94rem;
        }
            background-color: rgba(239, 98, 98, 0.12);
            border-color: rgba(239, 98, 98, 0.24);
            color: #ffd0d0;
        .card p {
            margin: 0.16rem 0;
            color: var(--alab-text-2);
            font-size: 0.81rem;
            background-color: rgba(228, 182, 76, 0.12);
            border-color: rgba(228, 182, 76, 0.22);
            color: #ffe3a0;

        .alab-card-seen,
        .card.visto {
            opacity: 0.84;
            background-color: rgba(37, 184, 106, 0.12);
            border-color: rgba(37, 184, 106, 0.22);
            color: #c8f0d8;

        .alab-badge-vencido,
        .vencido {
            background-color: rgba(139, 0, 0, 0.88);
            background-color: rgba(78, 161, 255, 0.12);
            border-color: rgba(78, 161, 255, 0.22);
            color: #cfe6ff;
        }

        .stApp [data-testid="stAlert"] {
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: rgba(18, 22, 29, 0.94);
        }

        .stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
            color: var(--alab-text-1) !important;
        }

        .stApp .stDataFrame,
        .stApp [data-testid="stTable"] {
            border: 1px solid var(--alab-border);
            border-radius: var(--alab-radius-md);
            overflow: hidden;
            background: rgba(15, 17, 22, 0.96);
        }

        .stApp .ag-root-wrapper,
        .stApp .ag-theme-streamlit,
        .stApp .ag-theme-alpine,
        .stApp .ag-theme-balham {
            border: 1px solid var(--alab-border) !important;
            border-radius: var(--alab-radius-md) !important;
            background: rgba(15, 17, 22, 0.96) !important;
            color: var(--alab-text-1) !important;
        }

        .stApp .ag-header,
        .stApp .ag-header-viewport,
        .stApp .ag-header-container {
            background: #14171d !important;
            border-bottom: 1px solid var(--alab-border) !important;
        }

        .stApp .ag-header-cell,
        .stApp .ag-header-group-cell {
            border-right: 0 !important;
            color: var(--alab-text-3) !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase;
        }

        .stApp .ag-row {
            background: rgba(15, 17, 22, 0.98) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            color: var(--alab-text-1) !important;
        }

        .stApp .ag-row:hover {
            background: rgba(255, 255, 255, 0.025) !important;
        }

        .stApp .ag-row-selected,
        .stApp .ag-row.ag-row-focus {
            background: rgba(37, 184, 106, 0.1) !important;
        }

        .stApp .ag-cell {
            border-right: 0 !important;
            display: flex;
            align-items: center;
            color: var(--alab-text-2) !important;
        }

        .stApp .ag-paging-panel,
        .stApp .ag-status-bar,
        .stApp .ag-menu,
        .stApp .ag-popup,
        .stApp .ag-panel {
            background: var(--alab-surface-2) !important;
            color: var(--alab-text-1) !important;
            border-color: var(--alab-border) !important;
        }

        .stApp .js-plotly-plot .plotly .modebar {
            background: rgba(18, 22, 29, 0.84) !important;
            border: 1px solid var(--alab-border) !important;
            border-radius: 10px;
        }

        .alab-footer {
            margin-top: 1.1rem;
            padding-top: 0.95rem;
            border-top: 1px solid var(--alab-border);
        }

        .alab-footer-inner {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            padding: 0.9rem 1rem;
            border-radius: var(--alab-radius-md);
            border: 1px solid var(--alab-border);
            background: linear-gradient(180deg, rgba(18, 22, 29, 0.92), rgba(15, 18, 24, 0.98));
        }

        .alab-footer-main {
            min-width: 0;
        }

        .alab-footer-side {
            flex: 0 0 auto;
            text-align: right;
        }

        .alab-footer-title {
            color: var(--alab-text-1);
            font-family: 'Sora', sans-serif;
            font-size: 0.92rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .alab-footer-copy {
            color: var(--alab-text-2);
            font-size: 0.78rem;
            margin: 0.08rem 0;
        }

        .alab-footer-meta {
            color: var(--alab-text-4);
            font-size: 0.72rem;
            margin-top: 0.08rem;
        }

        .alab-badge-vencido,
        .vencido {
            background-color: rgba(239, 98, 98, 0.12);
            border-color: rgba(239, 98, 98, 0.24);
            color: #ffd0d0;
        }

        .alab-badge-hoy,
        .hoy {
            background-color: rgba(228, 182, 76, 0.12);
            border-color: rgba(228, 182, 76, 0.24);
            color: #ffe3a0;
        }

        .alab-badge-proximo,
        .proximo {
            background-color: rgba(37, 184, 106, 0.12);
            border-color: rgba(37, 184, 106, 0.24);
            color: #c8f0d8;
        }

        .alab-badge-futuro,
        .futuro {
            background-color: rgba(78, 161, 255, 0.12);
            border-color: rgba(78, 161, 255, 0.24);
            color: #cfe6ff;
        }

        @media (max-width: 1024px) {
            .alab-kpi-grid,
            .kpi-container,
            .alab-mini-grid {
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            }

            [data-testid="stAppViewContainer"] .block-container {
                padding-right: 1.4rem;
                padding-left: 1.4rem;
            }

            .alab-player-media-row {
                width: 100%;
                justify-content: flex-start;
                flex-wrap: wrap;
            }

            .alab-detail-grid {
                grid-template-columns: 1fr;
            }

            .alab-footer-inner {
                flex-direction: column;
                align-items: flex-start;
            }

            .alab-footer-side {
                text-align: left;
            }

            .alab-top-rank-group {
                margin-bottom: 0.65rem;
            }
        }

        @media (max-width: 768px) {
            [data-testid="stAppViewContainer"] .block-container {
                padding-top: 1rem;
                padding-right: 1rem;
                padding-left: 1rem;
            }

            .alab-kpi-grid,
            .kpi-container,
            .alab-mini-grid,
            .alab-detail-grid {
                grid-template-columns: 1fr;
            }

            .alab-dashboard-chip-row {
                gap: 0.4rem;
            }

            .alab-player-photo,
            .alab-player-photo-placeholder {
                width: 132px;
            }

            .alab-panel-title.alab-top-rank-title,
            .panel-title.alab-top-rank-title {
                white-space: normal;
                line-height: 1.25;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )