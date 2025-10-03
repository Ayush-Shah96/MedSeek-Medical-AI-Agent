# File: app.py
import gradio as gr
from routes.main import create_interface

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
