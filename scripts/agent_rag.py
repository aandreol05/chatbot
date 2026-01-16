import os
import json
from datetime import datetime

import requests
from agents import Agent, function_tool, Runner
from dotenv import load_dotenv
from upstash_vector import Index
from typing import Dict, Optional

load_dotenv(override=True)
index = Index.from_env()

# =========================
# Tool : recherche vectorielle
# =========================

@function_tool
def search_index(query: str) -> str:
    """
    Recherche vectorielle dans l'index Upstash à partir d'un mot ou d'une phrase
    issue de la question utilisateur.

    Retourne toujours un dictionnaire structuré afin de faciliter
    la génération d'une phrase par le LLM.
    """

    query_result = index.query(
        data=query,
        include_metadata=True,
        include_data=True,
        top_k=5,
    )

    return "\n\n".join([result.data for result in query_result])


# =========================
# Agent
# =========================

agent = Agent(
    name="Andrea agent",
    model="gpt-4.1-nano",
    tools=[search_index],
    instructions="Tu es Andrea, ton objectif est de répondre aux questions de l'utilisteur sur ton profil professionel. Répond uniquement à la question de l'utilisateur. Sois concis. Donne toute les infos que tu trouves et mes les dans le bon ordres selon la pertinence. Tu peux utiliser l'outil search_index pour t'aider à trouver des informations pertinentes sur ton profil. N'invente pas d'informations. Si tu ne trouves pas la réponse dans les résultats de recherche, répond que tu ne sais pas.",
)

result = Runner.run_sync(agent, "quel sont tes projets ?")
print(result.final_output)