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
            --brand-soft: rgba(90, 154, 124, 0.16);
            --brand-soft-strong: rgba(90, 154, 124, 0.28);
            --brand-line: rgba(90, 154, 124, 0.34);
            --panel-top: rgba(27, 51, 42, 0.84);
            --panel-bottom: rgba(10, 26, 20, 0.94);
            --panel-strong: rgba(14, 24, 20, 0.94);
            --panel-blue: rgba(30, 60, 114, 0.2);
            --text-1: rgba(255, 255, 255, 0.96);
            --text-2: rgba(226, 236, 231, 0.78);
            --text-3: rgba(193, 208, 200, 0.58);
            --danger: #ff6f61;
            --warning: #ffd700;
            --radius-xl: 24px;
            --radius-lg: 18px;
            --radius-md: 14px;
            --radius-sm: 10px;
            --space-1: 0.35rem;
            --space-2: 0.55rem;
            --space-3: 0.85rem;
            --space-4: 1.1rem;
            --space-5: 1.5rem;
            --space-6: 2rem;
            --shadow-lg: 0 22px 64px rgba(0, 0, 0, 0.42);
            --shadow-md: 0 14px 36px rgba(0, 0, 0, 0.34);
            --shadow-sm: 0 10px 24px rgba(0, 0, 0, 0.24);
            --transition: 180ms ease;
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
            position: relative;
            background:
                radial-gradient(circle at 18% 14%, rgba(90, 154, 124, 0.2), transparent 34%),
                radial-gradient(circle at 84% 24%, rgba(58, 102, 81, 0.34), transparent 30%),
                radial-gradient(circle at 52% 100%, rgba(90, 154, 124, 0.1), transparent 36%),
                linear-gradient(135deg, #3a6651 0%, #1a3a2a 44%, #0a1a14 100%);
            background-attachment: fixed;
            color: var(--text-1);
            overflow-x: hidden;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 32px 32px;
            mask-image: radial-gradient(circle at center, black 38%, transparent 100%);
            opacity: 0.32;
        }

        [data-testid="stAppViewContainer"],
        section[data-testid="stSidebar"] {
            --primary-color: #5a9a7c !important;
            --primary-color-hover: #5a9a7c !important;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1540px;
            padding-top: 1.15rem;
            padding-bottom: 2.4rem;
        }

        div[data-testid="stVerticalBlock"] {
            gap: var(--space-4);
        }

        hr {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            margin: 0.4rem 0 0.9rem;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: var(--text-1) !important;
            font-family: 'Sora', sans-serif !important;
            letter-spacing: -0.025em;
            line-height: 1.1;
            margin-bottom: 0.3rem;
        }

        h1 {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
        }

        h2 {
            font-size: 1.55rem !important;
            font-weight: 700 !important;
        }

        h3 {
            font-size: 1.18rem !important;
            font-weight: 700 !important;
        }

        h4,
        h5,
        h6,
        label,
        .stMarkdown,
        .stCaption,
        p {
            color: var(--text-2) !important;
        }

        p,
        li,
        label,
        .stMarkdown,
        [data-testid="stMetricLabel"],
        [data-testid="stCaptionContainer"] {
            font-size: 0.96rem;
            line-height: 1.55;
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

        div[data-testid="stContainer"],
        div[data-testid="stForm"],
        details[data-testid="stExpander"],
        div[data-testid="stDataFrame"],
        div[data-testid="stMetric"],
        div[data-testid="stPlotlyChart"],
        div.stImage {
            background:
                linear-gradient(180deg, rgba(30, 60, 114, 0.1), transparent 42%),
                linear-gradient(160deg, var(--panel-top), var(--panel-bottom));
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            backdrop-filter: blur(14px);
        }

        div[data-testid="stContainer"] {
            padding: var(--space-4);
            margin-bottom: var(--space-3);
        }

        div[data-testid="stForm"],
        details[data-testid="stExpander"],
        div[data-testid="stDataFrame"],
        div[data-testid="stMetric"],
        div[data-testid="stPlotlyChart"] {
            overflow: hidden;
        }

        details[data-testid="stExpander"] {
            padding: 0 !important;
        }

        details[data-testid="stExpander"] summary {
            background: rgba(255, 255, 255, 0.02);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: var(--radius-lg);
            padding: 0.9rem 1.05rem;
            font-weight: 700;
            color: var(--text-1) !important;
        }

        details[data-testid="stExpander"] summary:hover {
            background: rgba(255, 255, 255, 0.04);
        }

        details[data-testid="stExpander"] > div {
            padding: 0.9rem 1rem 1rem;
        }

        [data-testid="stMetric"] {
            min-height: 128px;
            padding: 1rem 1.05rem;
            position: relative;
        }

        [data-testid="stMetric"]::after {
            content: "";
            position: absolute;
            inset: auto 16px 0 16px;
            height: 3px;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(90, 154, 124, 0.75), rgba(90, 154, 124, 0.08));
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-3) !important;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] {
            color: var(--text-1) !important;
            font-family: 'Sora', sans-serif !important;
            font-size: 2rem !important;
            font-weight: 800 !important;
            line-height: 1;
        }

        [data-testid="stMetricDelta"] {
            color: var(--brand) !important;
            font-weight: 700;
        }

        .kpi-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1rem;
            margin: 1rem 0 1.7rem;
        }

        .kpi-card,
        .card {
            position: relative;
            background:
                linear-gradient(180deg, rgba(30, 60, 114, 0.12), transparent 44%),
                linear-gradient(140deg, rgba(58, 102, 81, 0.9), rgba(10, 26, 20, 0.96));
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            overflow: hidden;
        }

        .kpi-card::before,
        .card::before,
        .rank-card::before,
        .player-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), transparent 34%);
            pointer-events: none;
        }

        .kpi-card {
            padding: 1.15rem 1.15rem 1rem;
            min-width: 220px;
            text-align: left;
            transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
        }

        .kpi-card:hover,
        .rank-card:hover,
        .player-card:hover,
        .card:hover {
            transform: translateY(-3px);
            border-color: var(--brand-line);
            box-shadow: var(--shadow-lg);
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
            position: relative;
            background: linear-gradient(120deg, rgba(58, 102, 81, 0.86), rgba(10, 26, 20, 0.94));
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: var(--radius-md);
            padding: 0.85rem 1rem;
            margin-bottom: 0.55rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow-sm);
            transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
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

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            width: 100%;
            min-height: 44px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: linear-gradient(180deg, rgba(90, 154, 124, 0.18), rgba(58, 102, 81, 0.16));
            color: var(--text-1);
            font-weight: 700;
            letter-spacing: 0.01em;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05), var(--shadow-sm);
            transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition), background var(--transition);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-1px);
            border-color: var(--brand-line);
            background: linear-gradient(180deg, rgba(90, 154, 124, 0.26), rgba(58, 102, 81, 0.22));
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), var(--shadow-md);
        }

        .stButton > button[kind="primary"],
        .stDownloadButton > button[kind="primary"],
        div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
            background: linear-gradient(180deg, rgba(90, 154, 124, 0.92), rgba(58, 102, 81, 0.94));
            border-color: rgba(90, 154, 124, 0.8);
            color: #ffffff;
        }

        .stButton > button[kind="primary"]:hover,
        .stDownloadButton > button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
            background: linear-gradient(180deg, rgba(107, 171, 140, 0.98), rgba(58, 102, 81, 0.98));
        }

        .stButton > button:disabled,
        div[data-testid="stFormSubmitButton"] > button:disabled {
            opacity: 0.45;
            cursor: not-allowed;
            box-shadow: none;
        }

        *:focus,
        *:focus-visible {
            outline: none !important;
        }

        input,
        textarea {
            caret-color: var(--brand) !important;
            color: var(--text-1) !important;
        }

        input::placeholder,
        textarea::placeholder {
            color: var(--text-3) !important;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div,
        .stDateInput > div > div,
        .stNumberInput > div > div {
            min-height: 46px;
            border: 1px solid rgba(90, 154, 124, 0.28) !important;
            border-radius: 12px !important;
            background: linear-gradient(180deg, rgba(14, 24, 20, 0.9), rgba(10, 26, 20, 0.84)) !important;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
            color: var(--text-1) !important;
            transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
        }

        div[data-baseweb="input"] > div:hover,
        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="textarea"] > div:hover,
        .stDateInput > div > div:hover,
        .stNumberInput > div > div:hover {
            border-color: rgba(90, 154, 124, 0.42) !important;
        }

        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within,
        .stDateInput > div > div:focus-within,
        .stNumberInput > div > div:focus-within {
            border-color: var(--brand) !important;
            box-shadow: 0 0 0 1px rgba(90, 154, 124, 0.25), 0 0 0 6px rgba(90, 154, 124, 0.08) !important;
            background: linear-gradient(180deg, rgba(14, 24, 20, 0.98), rgba(10, 26, 20, 0.92)) !important;
        }

        div[aria-invalid="true"],
        div[aria-invalid="true"] * {
            border-color: var(--brand) !important;
            box-shadow: 0 0 0 1px rgba(90, 154, 124, 0.25), 0 0 0 6px rgba(90, 154, 124, 0.08) !important;
        }

        [data-baseweb="tag"] {
            background: rgba(90, 154, 124, 0.16) !important;
            border: 1px solid rgba(90, 154, 124, 0.3) !important;
            border-radius: 999px !important;
            color: var(--text-1) !important;
        }

        .stSlider label,
        .stSlider span,
        .stSlider [data-testid="stSliderThumbValue"] {
            color: var(--text-2) !important;
            font-weight: 700;
        }

        .stSlider div[data-baseweb="slider"] > div {
            background-color: rgba(10, 26, 20, 0.82) !important;
            border-radius: 999px;
            min-height: 6px;
        }

        .stSlider div[data-baseweb="slider"] > div > div {
            background: linear-gradient(90deg, #5a9a7c, #3a6651) !important;
            border-radius: 999px;
        }

        .stSlider [role="slider"] {
            width: 18px !important;
            height: 18px !important;
            background-color: var(--brand) !important;
            border: 2px solid #ffffff !important;
            box-shadow: 0 0 0 4px rgba(90, 154, 124, 0.12), 0 0 12px rgba(90, 154, 124, 0.45) !important;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(58, 102, 81, 0.18), transparent 16%),
                linear-gradient(180deg, #0a1a14, #1a3a2a);
            border-right: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 18px 0 40px rgba(0, 0, 0, 0.22);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: var(--text-1) !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 0.25rem;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label {
            margin: 0.15rem 0;
            padding: 0.72rem 0.82rem;
            border: 1px solid transparent;
            border-radius: 12px;
            background: transparent;
            transition: background var(--transition), border-color var(--transition), transform var(--transition);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.06);
            transform: translateX(2px);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-selected="true"] {
            background: linear-gradient(90deg, rgba(90, 154, 124, 0.22), rgba(90, 154, 124, 0.05));
            border: 1px solid rgba(90, 154, 124, 0.26);
            box-shadow: inset 4px 0 0 #5a9a7c;
        }

        div[role="radiogroup"] label span div {
            background-color: var(--brand) !important;
        }

        div[role="radiogroup"] label span[aria-hidden="true"] {
            border-color: var(--brand) !important;
        }

        div[data-testid="stDataFrame"] {
            padding: 0.5rem;
        }

        div[data-testid="stDataFrame"] table {
            background: transparent !important;
            color: var(--text-1) !important;
            border-collapse: separate !important;
            border-spacing: 0;
        }

        div[data-testid="stDataFrame"] thead th {
            background: rgba(255, 255, 255, 0.04) !important;
            color: var(--brand) !important;
            font-size: 0.78rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        div[data-testid="stDataFrame"] tbody td {
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            color: var(--text-2) !important;
            font-size: 0.93rem !important;
        }

        div[data-testid="stDataFrame"] tbody tr:hover td {
            background: rgba(90, 154, 124, 0.12) !important;
            color: #ffffff !important;
        }

        div[data-testid="stPlotlyChart"] {
            padding: 0.9rem;
        }

        .js-plotly-plot .plotly,
        .js-plotly-plot .plot-container {
            border-radius: 16px;
        }

        .stAlert {
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        .stAlert.success {
            background-color: rgba(0, 51, 102, 0.97) !important;
            color: var(--brand) !important;
            border-left: 4px solid var(--brand) !important;
        }

        .stAlert.warning {
            background-color: rgba(51, 43, 0, 0.97) !important;
            color: var(--warning) !important;
            border-left: 4px solid var(--warning) !important;
        }

        .stAlert.error {
            background-color: rgba(51, 0, 0, 0.97) !important;
            color: var(--danger) !important;
            border-left: 4px solid var(--danger) !important;
        }

        .player-card {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.8rem;
            width: 100%;
            min-height: 82px;
            margin: 0.35rem auto;
            padding: 0.85rem 0.95rem;
            background: linear-gradient(130deg, rgba(58, 102, 81, 0.88), rgba(10, 26, 20, 0.95));
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
        }

        .player-photo {
            width: 56px;
            height: 56px;
            border-radius: 16px;
            object-fit: cover;
            border: 1px solid rgba(90, 154, 124, 0.55);
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.28);
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

        .player-link a:hover {
            text-decoration: underline;
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
            transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
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
            opacity: 0.82;
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
            .block-container {
                padding-top: 0.85rem;
            }

            [data-testid="stMetricValue"] {
                font-size: 1.7rem !important;
            }

            .kpi-container {
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            }
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 1.8rem !important;
            }

            h2 {
                font-size: 1.35rem !important;
            }

            div[data-testid="stContainer"],
            div[data-testid="stForm"],
            details[data-testid="stExpander"] > div,
            div[data-testid="stPlotlyChart"] {
                padding-left: 0.85rem;
                padding-right: 0.85rem;
            }

            .player-card,
            .card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
