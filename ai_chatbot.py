import fitz
import gradio as gr
from openai import OpenAI

client = OpenAI()


def chatbot(pdf_file, question):
    doc = fitz.open(pdf_file.name)
    text = ""


    for page in doc:
        text += page.get_text()

    doc.close()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system", "content": "You are a helpful assistant. Answer questions based on the document provided."},

            {
                "role": "user",
                "content": f"DOCUMENT:\n{text[:4000]}\n\nQUESTION:\n{question}"
            }
        ]
    )

    return response.choices[0].message.content


# Launch UI
gr.Interface(
    fn=chatbot,
    inputs=["file", "text"],
    outputs="text",
    title="My PDF Chatbot 🤖"
).launch()