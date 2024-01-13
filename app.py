import os

import gradio as gr
from langchain.chains import RetrievalQA
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAI
from openai import OpenAI as OpenAIClient

import hpqa

os.environ["OPENAI_API_KEY"] = ""
index_path = hpqa.LOCAL_DATA_PATH / "hpqa_faiss_index_500"


examples = [
    "How would you sneak into Hogwarts without being detected?",
    "Why did Snape kill Dumbledore?",
    "Who is the most badass wizard in the world?",
    "Who would win a fight between Dumbledore and a grizzly bear?",
    "How many siblings does Hermione have?",
    "Why are the Dursleys so mean to Harry?",
]


def api(question, temperature, model, api_key=None):
    if api_key is None or len(api_key) == 0:
        return "You must provide an OpenAI API key to use this demo 👇"
    if len(question) == 0:
        return ""
    document_store = hpqa.load_document_store(index_path, openai_api_key=api_key)

    client = OpenAIClient(api_key=api_key)
    models = [m.id for m in client.models.list().data if "gpt" in m.id if "vision" not in m.id]
    if model not in models:
        model_list = "\n".join(models)
        return f"😬 {model} not a valid model name. Choose from:\n\n{model_list}"

    chain = RetrievalQA.from_llm(
        llm=OpenAI(temperature=temperature, openai_api_key=api_key),
        retriever=VectorStoreRetriever(vectorstore=document_store),
    )
    response = chain.invoke(question)
    return response["result"].strip()


demo = gr.Blocks()

with demo:
    gr.Markdown("# 🪄 The GPT Who Lived: Harry Potter QA with GPT 🤖")
    with gr.Row():
        with gr.Column():
            question = gr.Textbox(lines=4, label="Question")
            temperature = gr.Slider(0.0, 2.0, 0.7, step=0.1, label="🍺 Butterbeer Consumed")
            with gr.Row():
                clear = gr.Button("Clear")
                btn = gr.Button("Submit", variant="primary")
        with gr.Column():
            answer = gr.Textbox(lines=4, label="Answer")
            with gr.Row():
                model = gr.Textbox(value="gpt-3.5-turbo-instruct", label="OpenAI Model")
                openai_api_key = gr.Textbox(type="password", label="OpenAI API key")
    btn.click(api, [question, temperature, model, openai_api_key], answer)
    clear.click(lambda _: "", question, question)
    gr.Examples(examples, question)
    gr.Markdown("💻 Checkout the `hpqa` source code on [GitHub](https://github.com/johnnygreco/hpqa).")
demo.launch()
