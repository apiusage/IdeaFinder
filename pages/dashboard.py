from config.settings import Idea_Excel_File
from utils.utils import show_csv
from services.paywallscreens import scrape_paywallscreens
import streamlit as st


def run_dashboard():
    show_csv(Idea_Excel_File)

    df = scrape_paywallscreens()

    print(df.head())

    df.to_csv(
        "paywallscreens.csv",
        index=False
    )