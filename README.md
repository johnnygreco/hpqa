# `hpqa` – 🪄 Harry Potter QA with GPT 🤖

![harry-potter-sorcerer-stone](https://user-images.githubusercontent.com/10998105/217035363-3d079a9e-3333-4e5d-a2a6-98972060c071.gif)

---

# Overview

This application gives [OpenAI's GPT-3](https://platform.openai.com/docs/models/gpt-3) access to all the Harry Potter books (plus the associated Wikipedia plot summaries) and lets you ask it questions. You can give the model more butterbeer (i.e., increase the temperature 😉) to make its answers more unpredictable 🍻.

Under the hood, we index the text using [Faiss](https://github.com/facebookresearch/faiss) and streamline interactions with GPT using [LangChain](https://github.com/hwchase17/langchain).

**Note:** To use the app, you'll need an [OpenAI API key](https://openai.com/api/). 

## Try the app on 🤗 Spaces 
👉  [https://huggingface.co/spaces/johnnygreco/the-gpt-who-lived](https://huggingface.co/spaces/johnnygreco/the-gpt-who-lived)


# Installation
```shell
git clone https://github.com/johnnygreco/hpqa.git
cd hpqa
python -m pip install -e .
```

# Running the app
```shell
python app.py
```

<img width="1000" alt="gradio-demo" src="https://github.com/johnnygreco/hpqa/assets/10998105/60d52b20-bd8a-468c-84d0-8191057c15b0">
