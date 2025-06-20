# llm_utils.py

import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement dès l'importation du module
load_dotenv()

def generate_and_format_response(
    provider,
    model,
    messages,
    temperature=0.7,
    max_tokens=1500,
    top_p=0.9,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    min_tokens=None,
    stream=False,
    stop=None,
    random_seed=None,
    response_format=None,
    tools=None,
    tool_choice="auto",
    safe_prompt=False
):
    """
    Génère et formate une réponse à partir du fournisseur LLM spécifié (OpenAI, Anthropic ou Mistral).

    Paramètres :
    - provider (str) : Le fournisseur LLM à utiliser ("openai", "anthropic" ou "mistral").
    - model (str) : Le modèle à utiliser pour la génération de texte.
    - messages (list) : Une liste de messages au format [{"role": "user", "content": "Votre prompt ici"}].
    - temperature (float, optionnel) : Contrôle la randomisation dans la sortie (par défaut : 0.7 pour Anthropic & Mistral, 1.0 pour OpenAI).
    - max_tokens (int, optionnel) : Nombre maximum de tokens à générer (par défaut : 1500).
    - top_p (float, optionnel) : Paramètre de nucleus sampling pour contrôler la diversité (par défaut : 0.9).
    - frequency_penalty (float, optionnel) : Pénalise les nouveaux tokens en fonction de la fréquence (OpenAI uniquement).
    - presence_penalty (float, optionnel) : Pénalise les nouveaux tokens en fonction de la présence (OpenAI uniquement).
    - ... (autres paramètres spécifiques aux fournisseurs)

    Retour :
    - formatted_text (str) : La réponse formatée de l'assistant en Markdown.
    """

    api_key = None
    url = None
    headers = {"Content-Type": "application/json"}

    # Déterminer la clé API, le point de terminaison et les en-têtes en fonction du fournisseur
    if provider.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        url = "https://api.openai.com/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }

    elif provider.lower() == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        url = "https://api.anthropic.com/v1/messages"
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01"
        payload = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "messages": messages
        }

    elif provider.lower() == "mistral":
        api_key = os.getenv("MISTRAL_API_KEY")
        url = "https://api.mistral.ai/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "tool_choice": tool_choice,
            "safe_prompt": safe_prompt
        }
        # Ajouter les paramètres optionnels pour Mistral
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if min_tokens is not None:
            payload["min_tokens"] = min_tokens
        if stop is not None:
            payload["stop"] = stop
        if random_seed is not None:
            payload["random_seed"] = random_seed
        if response_format is not None:
            payload["response_format"] = response_format
        if tools is not None:
            payload["tools"] = tools
    else:
        return "Fournisseur invalide. Veuillez choisir parmi 'openai', 'anthropic' ou 'mistral'."

    # Vérifier si la clé API est disponible
    if not api_key:
        raise ValueError(f"Clé API {provider.capitalize()} introuvable. Veuillez la définir dans le fichier .env.")

    try:
        # Envoyer la requête POST à l'API du fournisseur
        response = requests.post(url, headers=headers, json=payload)
        
        # Lever une exception si la requête a échoué
        response.raise_for_status()
        
        # Analyser la réponse JSON
        response_data = response.json()
        
        # Extraire le message de l'assistant et les informations sur les tokens en fonction du fournisseur
        input_tokens = len(" ".join(msg["content"] for msg in messages).split())  # Estimation des tokens d'entrée
        if provider.lower() == "openai":
            assistant_message = response_data["choices"][0]["message"]["content"].strip()
            output_tokens = response_data["usage"]["completion_tokens"]

        elif provider.lower() == "anthropic":
            assistant_message = response_data.get("content", [{}])[0].get("text", "Aucune réponse trouvée.")
            output_tokens = len(assistant_message.split())  # Estimation des tokens de sortie

        elif provider.lower() == "mistral":
            assistant_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "Aucune réponse trouvée.")
            output_tokens = len(assistant_message.split())  # Estimation des tokens de sortie
        
        # Formater la réponse incluant le fournisseur, le modèle et les informations sur les tokens
        formatted_text = (
            f"**Fournisseur :** {provider.capitalize()} | **Modèle :** {model}  \n"
            f"**Tokens Utilisés (Entrée/Sortie) :** {input_tokens}/{output_tokens}  \n\n"
            f"**Assistant :**\n\n{assistant_message}\n"
        )
        return formatted_text

    except requests.exceptions.RequestException as e:
        return f"Une erreur est survenue : {e}"

