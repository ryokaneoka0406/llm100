import streamlit as st
from openai import OpenAI
import json

st.title('Quiz UI generator with JSON mode')

# env variables
user_api_key = st.sidebar.text_input(
    label="OpenAI API key",
    placeholder="Paste your OpenAI API key here",
    type="password")

# user input
user_prompt = st.text_area(
    label="Prompt",
    placeholder="Write topic here",
    height=200)

def generate_quiz_ui(topic, api_key):
    client = OpenAI(
            api_key=api_key
        )

    assistant_prompt = """
    {
        "quizzes": [
            {
            "id": Number,
            "question": String,
            "question_items": [
                {
                "id": Number,
                "question_item": String
                }
            ]
            }
        ]
    }
    """

    PROMPT = f"""
        You are an assistant tasked with creating about five multiple-choice quizzes
        from a topic given in JSON format.
        Please respond in JSON format.

        ## Quiz
        {topic}

        ## JSON Format
        "question_id": The ID of the question, in sequential order starting from 1.
        "question": The text of the question.
        "question_items": An array of options for the question.
        "question_item_id": The ID of the question option, in sequential order starting from 1.
        "question_item": The option of the question.
        """

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            { 'role': 'assistant', 'content': assistant_prompt },
            {"role": "user", "content": PROMPT}
        ]

    )
    result = response.choices[0].message.content

    return result

if st.button("genarate"):
    with st.spinner("Loading..."):
        result = generate_quiz_ui(user_prompt, user_api_key)

        data = json.loads(result)

        # Iterate over the quizzes
        for quiz in data['quizzes']:
            st.radio(
                quiz['question'],
                [item['question_item'] for item in quiz['question_items']],
                index=None)