from   app.interface.Streamlit import StreamlitUI
import streamlit as st
import logging
import sys
import os


# Add the root of your project (file_organiser/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Application entry point."""
    try:
        app = StreamlitUI()
        app.render()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()