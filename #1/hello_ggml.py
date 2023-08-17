from llama_cpp import Llama
import streamlit as st

# LLMの準備


def run_llama(prompt):
    llm = Llama(model_path="llama-2-7b-chat.ggmlv3.q8_0.bin")
    output = llm(
        prompt,
        max_tokens=32,
        stop=["Instruction:", "Input:", "Response:", "\n"],
        echo=True,
    )
    return output


st.subheader("Running Llama2 locally")
prompt = st.text_area(
    "prompt")

if st.button("Run"):
    with st.spinner("Running..."):
        try:
            output = run_llama(prompt)
            st.success(output["choices"][0]["text"])
        except Exception as e:
            st.error(e)
