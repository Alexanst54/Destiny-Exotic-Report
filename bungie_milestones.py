import requests

# clé API Bungie
API_KEY = ""

# Headers pour l'authentification
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Étape 1 : Rechercher le joueur par nom
def search_player(display_name):
    # Découper le display name en nom et code
    if '#' not in display_name:
        raise Exception("Le display name doit être au format Nom*#Code")
    name, code = display_name.split('#', 1)
    url = "https://www.bungie.net/Platform/User/Search/GlobalName/0/"
    payload = {
        "displayName": name,
        "displayNameCode": int(code)
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    try:
        response.raise_for_status()
        results = response.json()
        player = results['Response']['searchResults'][0]['destinyMemberships'][0]
        return player['membershipType'], player['membershipId'], player['displayName']
    except (IndexError, KeyError):
        raise Exception("Joueur introuvable ou réponse invalide.")
    except Exception as e:
        raise Exception(f"Erreur lors de la recherche du joueur : {e}")

# Étape 2 : Récupérer les milestones du joueur
def get_milestones(membership_type, membership_id):
    url = f"https://www.bungie.net/Platform/Destiny2/{membership_type}/Profile/{membership_id}/?components=202"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Étape 3 : Afficher les activités des milestones
def display_milestone_activities(milestone_data):
    milestones = milestone_data.get("Response", {}).get("milestones", {})
    if not milestones:
        print("Aucun milestone trouvé.")
        return
    for milestone_hash, milestone in milestones.items():
        print(f"Milestone Hash: {milestone_hash}")
        activities = milestone.get("activities", [])
        for activity in activities:
            print(f"  Activity Hash: {activity.get('activityHash')}")

# Exécution principale
if __name__ == "__main__":
    display_name = "Alex*#2048"
    try:
        membership_type, membership_id, name = search_player(display_name)
        print(f"Joueur trouvé : {name} (Type: {membership_type}, ID: {membership_id})")
        milestone_data = get_milestones(membership_type, membership_id)
        display_milestone_activities(milestone_data)
    except Exception as e:
        print(f"Erreur : {e}")
