from argparse import ArgumentParser

import gradio as gr
from haystack.nodes.prompt import PromptNode

import hpqa

parser = ArgumentParser()
parser.add_argument("--model-size", default="xl", help="Model size of Flan-T5 [base, large, or xl]")
args = parser.parse_args()
assert args.model_size in ["base", "large", "xl"]

hpqa.LOCAL_DATA_PATH.mkdir(exist_ok=True)
index_path = hpqa.LOCAL_DATA_PATH / "index.faiss"


if not index_path.exists():
    print("Creating Harry Potter book embeddings and indexing document store. This will take a few minutes.")
    db_path = hpqa.LOCAL_DATA_PATH / "faiss_document_store.db"
    document_store, retriever = hpqa.build_document_store(db_path, index_path)
else:
    document_store, retriever = hpqa.load_document_store(index_path)

model_name = f"google/flan-t5-{args.model_size}"

print(f"Loading LLM: {model_name}")
prompt_node = PromptNode(model_name_or_path=model_name, default_prompt_template="question-answering")


examples = [
    "What is the job of the sorting hat?",
    "Why does Snape kill Dumbledore?",
    "Why does Snape protect Harry?",
    "How many presents does Dudley get on his birthday?",
    "What time does the Hogwarts Express leave?",
    "What famous wizard card does Harry get in his first chocolate frog?",
    "Who would win a fight between Dumbledore and a grizzly bear?",
    "Who would win a fight between a muggle and a grizzly bear?",
    "What is a way to sneak into Hogwarts without being detected?",
    "Why do students make fun of Hermione?",
]


def api(question):
    docs = retriever.retrieve_batch([question])
    return prompt_node.prompt(prompt_template="question-answering", documents=docs, questions=[question])[0]


demo = gr.Interface(
    fn=api,
    inputs=gr.Textbox(lines=4, label="Question"),
    outputs=gr.Textbox(lines=4, label="Answer"),
    examples=examples,
    allow_flagging="auto",
    description=f"# 🪄 Harry Potter Question-Answering with 🍮-{args.model_size}",
)

demo.launch()
