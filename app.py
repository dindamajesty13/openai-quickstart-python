import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

@app.route("/chat", methods=("GET", "POST"))
def chat():
    if request.method == "POST":

        message = request.form["chat"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt_chat(message),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        return redirect(url_for("chat", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("chat.html", result=result)

def generate_prompt_chat(chat):
    return """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
    
    Human: Hello, who are you?
    AI: I am an AI created by OpenAI. How can I help you today?
    Human: {}.
    AI:""".format(chat)

@app.route("/story", methods=("GET", "POST"))
def story():
    if request.method == "POST":
        topic = request.form["topic"]
        sentence = request.form["sentence"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt_story(topic, sentence),
            temperature=0.8,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
        )
        return redirect(url_for("story", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("story.html", result=result)

def generate_prompt_story(topic, sentence):
    return """Topic: Breakfast
    Two-Sentence Horror Story: He always stops crying when I pour the milk on his cereal. I just have to remember not to let him see his face on the carton.
    
    Topic: {}
    Two-Sentence Horror Story:{}""".format(topic, sentence)
