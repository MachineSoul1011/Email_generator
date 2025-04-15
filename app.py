import streamlit as st
from openai import OpenAI
import os

# Set page configuration (this must be the first Streamlit command)
st.set_page_config(page_title="AI Email Generator", page_icon="✉️", layout="centered")

# Load API key
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Title & Description
st.title("✉️ AI Email Generator")
st.markdown("Create professional emails instantly with AI. Just fill in the details below:")

# --- Input Form ---
with st.form("email_form"):
    recipient = st.text_input("Recipient", placeholder="E.g., Hiring Manager, John Doe")
    subject = st.text_input("Subject", placeholder="E.g., Application for Frontend Developer Role")
    tone = st.selectbox("Tone", [
        "Formal", "Friendly", "Persuasive", "Apologetic", "Confident",
        "Casual", "Excited", "Grateful", "Urgent", "Supportive", "Encouraging"
    ])
    message_points = st.text_area("Key Points / Message Brief", placeholder="Mention key things to include in the email...")
    email_length = st.select_slider("Desired Email Length", options=["Short", "Medium", "Long"], value="Medium")
    font_style = st.selectbox("Choose Output Font", [
        "Default", "Monospace", "Serif", "Sans-Serif", "Georgia", "Verdana", "Tahoma"
    ])
    language = st.selectbox("Choose Language", ["English", "Spanish", "French", "German", "Hindi", "Mandarin", "Japanese"])

    submitted = st.form_submit_button("Generate Email")

# --- Processing ---
if submitted:
    if not OPENAI_API_KEY:
        st.error("🚫 OpenAI API key not found. Please set it using Streamlit Secrets or environment variable `OPENAI_API_KEY`.")
    elif not message_points.strip():
        st.warning("Please provide some message points to help the AI generate context.")
    else:
        with st.spinner("Generating your email..."):
            try:
                length_instruction = {
                    "Short": "Keep the email concise and under 100 words.",
                    "Medium": "Keep the email detailed but under 250 words.",
                    "Long": "Make the email comprehensive and elaborate fully."
                }[email_length]

                prompt = (
                    f"Write a {tone.lower()} email to {recipient} with the subject: '{subject}'. "
                    f"{length_instruction} Include the following points:\n{message_points.strip()}.\n\n"
                    f"Translate the email to {language}.\nSign off professionally."
                )

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=800,
                )

                email_text = response.choices[0].message.content.strip()

                st.success("✅ Email generated!")
                st.markdown("### 📧 Your Email")

                font_map = {
                    "Default": "inherit",
                    "Monospace": "'Courier New', monospace",
                    "Serif": "'Times New Roman', serif",
                    "Sans-Serif": "'Arial', sans-serif",
                    "Georgia": "'Georgia', serif",
                    "Verdana": "'Verdana', sans-serif",
                    "Tahoma": "'Tahoma', sans-serif"
                }

                st.markdown(
                    f"<div style='font-family: {font_map[font_style]}; white-space: pre-wrap; "
                    f"border: 1px solid #ddd; padding: 1rem; border-radius: 10px; background: #f9f9f9;'>"
                    f"{email_text}</div>",
                    unsafe_allow_html=True
                )

                st.download_button(
                    label="📥 Download Email as .txt",
                    data=email_text,
                    file_name="email.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
