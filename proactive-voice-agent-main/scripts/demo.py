"""Demo file to test different scenarios.

Run with:
```
poetry run python -m scripts.demo
```
"""

from app.llm import LlmClient
from app.schema import CustomLlmRequest

llm_client = LlmClient()
first_event = llm_client.greetings()


def complete_scenario(name, scenario):
    it_scenario = iter(scenario)
    transcript = []
    print(f"\n[BEGIN] scenario: {name}")
    try:
        while True:
            message = next(it_scenario)
            print(f"Message: {message}")
            transcript.append({"role": "user", "content": message})
            request = CustomLlmRequest(interaction_type="response_required", transcript=transcript)

            response = ""
            for event in llm_client.stream_response(request):
                response += event.content
            print(f"Response: {response}")
            transcript.append({"role": "agent", "content": response})
    except StopIteration:
        print(f"[END] scenario: {name}\n")
    except Exception as e:
        print(f"[Error]: {e}")


scenarios = {
    "prise_rdv_simple": [
        "Bonjour, je voudrais prendre rendez-vous pour un détartrage",
        "Sophie Martin",
        "Mardi prochain si possible",
        "11h ce serait parfait",
        "Oui confirmez s'il vous plaît"
    ],
    "urgence_dentaire": [
        "Bonjour, j'ai très mal aux dents, c'est urgent",
        "Thomas Dubois",
        "Le plus tôt possible, aujourd'hui si vous pouvez",
        "Oui 9h ça me va très bien merci"
    ],
    "question_puis_rdv": [
        "Bonjour, combien coûte un blanchiment dentaire ?",
        "D'accord, je voudrais prendre rendez-vous pour ça",
        "Marie Lambert",
        "Jeudi 14 novembre",
        "10h si c'est disponible",
        "Parfait, merci beaucoup"
    ],
    "questions_cabinet": [
        "Bonjour, vous êtes où exactement ?",
        "Vous êtes ouverts le samedi ?",
        "Vous prenez la carte bancaire ?",
        "Merci beaucoup, au revoir"
    ],
    "changement_horaire": [
        "Bonjour, je voudrais un rendez-vous pour des soins",
        "Jean Dupont",
        "Mercredi à 15h",
        "Non finalement, plutôt jeudi",
        "14h c'est possible ?",
        "Oui merci"
    ],
    "premiere_visite": [
        "Bonjour, c'est pour une première consultation",
        "Claire Rousseau",
        "Qu'est-ce que je dois apporter ?",
        "Vendredi matin si possible",
        "9h30 c'est parfait"
    ]
}

for name, scenario in scenarios.items():
    complete_scenario(name, scenario)
