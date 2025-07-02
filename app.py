import streamlit as st
import google.generativeai as genai
import os

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# Set up Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit app settings
st.set_page_config(page_title="Code Buddy – AI Code Explainer", page_icon="🤖")
st.title("👨‍💻 Code Buddy – Code Explainer")

st.markdown("Paste your code below. It will explain what it does and tell if there are bugs.")

# Input box for code
user_code = st.text_area("Paste your code here:", height=200, placeholder="e.g., def factorial(n): ...")

# When user clicks the button
if st.button("Explain Code"):
    if user_code.strip() == "":
        st.warning("Paste some code first.")
    else:
        prompt = f"""
You are a code expert.

Your job is to do two things:
1. Detect if the input is a valid code snippet in a known programming language like Python, Java, C++, JavaScript, etc.
2. If valid, explain clearly what the code does.
3. If the code has errors, identify and correct them.

⚠️ If the input is **not code**, say: "This doesn't appear to be valid code. Please try again."

Here is the input:
{user_code}
"""

        # Send request to Gemini
        with st.spinner("Analyzing code..."):
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🧠 Explanation:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
