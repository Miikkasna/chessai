import requests
import pandas as pd
from openai import AzureOpenAI
from secret import API_BASE, OPENAI_API_KEY
import json


gptclient = AzureOpenAI(
    api_key= OPENAI_API_KEY,
    api_version="2023-03-15-preview",
    azure_endpoint = API_BASE
    )


def ask_gpt(prompt):

    response = gptclient.chat.completions.create(
        model = "dataGPT",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000,
        top_p=0.95,
        frequency_penalty=0.9,
        presence_penalty=0,
        stop=None
        )
    result = response.choices[0].message.content
    return result


def get_a_move(board, player, last_move, error=""):
    prompt = f"""Given the board below, what is the best move for player {player}?\n
Give answer like this "||e3->e4||" (just an example, make your own move)\n
\n"""+ board + '\n' + error + '\n' + last_move
    print(prompt)
    response = ask_gpt(prompt)
    print(response)
    for i in range(6):
        try:
            response = response.split("||")[1]
            piece = response.split("->")[0]
            move = response.split("->")[1]
            return piece, move
        except:
            print("Error in response, trying again", i)
            response = ask_gpt(prompt)
    return "a1", "a2"
    

def get_move_comment(board, player, last_move):
    prompt = f"""{player} played {last_move} on the board below. Comment the move like chesscommentators!\n
\n"""+ board + '\n' + last_move
    print(prompt)
    response = ask_gpt(prompt)
    print(response)
    return response



