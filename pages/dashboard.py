from config.settings import Idea_Excel_File
from utils.utils import show_csv
import streamlit as st


def run_dashboard():
    show_csv(Idea_Excel_File)