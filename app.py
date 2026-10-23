import streamlit as st

st.set_page_config(layout="wide")

pages = [
    st.Page("HomePage.py", title="Home"),
    st.Page("RaceWatcherUI.py", title="Race Watcher")
]

st.markdown("""
    <style>
        [data-testid="stTopNavLink"] {
            color: #BDB8C9;
            background-color: transparent;
            padding: 0.4rem 0.8rem;
        }

        [data-testid="stTopNavLink"] p {
            color: #BDB8C9;
            font-size: 1.2rem;
        }

        [data-testid="stTopNavLink"][aria-current="page"] {
            color: #F5F3FA;
            background-color: #8A2BE2;
            padding: 0.6rem 1rem;
        }

        [data-testid="stTopNavLink"][aria-current="page"] p {
            color: #F5F3FA;
        }
    </style>
""", unsafe_allow_html=True)

TopBar = st.navigation(pages, position="top", expanded=True)
TopBar.run()