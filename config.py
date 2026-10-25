
import os
from dotenv import load_dotenv

load_dotenv()


def get_secret(name: str) -> str | None:
    # First, check local environment variables and .env
    value = os.getenv(name)

    if value:
        return value

    # Then, check Streamlit Cloud secrets
    try:
        import streamlit as st
        return st.secrets.get(name)
    except Exception:
        return None
