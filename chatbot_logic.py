import requests
from fuzzywuzzy import process


identified_med = [
    "Abilify", "Abilify Asimtufii", "Abilify Maintena", "Abiraterone", "Acetaminophen",
    "Acetylcysteine", "Actemra", "Actos", "Acyclovir", "Adderall",
    "Adderall XR", "Advair Diskus", "Advil", "Afinitor", "Agamree", "Aimovig", "Ajovy",
    "Albuterol", "Alecensa", "Alendronate", "Aleve", "Alfuzosin", "Allegra",
    "Allopurinol", "Alprazolam", "Alprolix", "Alunbrig", "Amantadine", "Ambien",
    "Ambroxol", "Amiodarone", "Amitriptyline", "Amlodipine"
]


# Function to fetch drug information from OpenFDA
def gettinginfo(med_name):
    # Encode drug name for URL
    encoded_drug = med_name.replace(' ', '+')
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{encoded_drug}&limit=1"

    try:
        reply = requests.get(url)
        reply.raise_for_status()  # Raise an exception for HTTP errors
        data = reply.json()

        if 'results' in data and data['results']:
            drug_info = data['results'][0]
            name = drug_info.get('openfda', {}).get('brand_name', ['Unknown'])[0]
            usage = drug_info.get('indications_and_usage', ['No usage information available'])[0]
            return f"{name}: {usage}"
        else:
            return "No information found!!! Try again."
    except requests.RequestException as e:
        return f"sorry. Couldn't fetch the data from API: {e}"


# Function to find the closest matching drug name
def Detect_closest_drug(user_input):
    nearest_pair, score = process.extractOne(user_input, identified_med)
    if score >= 80:  # Adjust threshold as needed
        return nearest_pair
    else:
        return None


# Define chatbot patterns and responses
def handle_chat(user_input):
    if user_input.lower() in ['quit', 'exit', 'bye']:
        return "See you again! Take care of your health"
    elif any(phrase in user_input for phrase in ['hello', 'hi', 'hey', 'greetings']):
        reply = "Hello! Kindly let me know what medicine you are looking for so I can assist you."
    elif any(phrase in user_input for phrase in ['no', 'not', 'nah', 'nope']):
        reply = ("I understand. My knowledge is limited to medicines and their uses."
                 " I cannot provide information on other topics.")
    elif any(phrase in user_input for phrase in ['thank you', 'thanks', 'thank', 'thx']):
        reply = "You're welcome! If you have any more questions, feel free to ask."
    else:
        closest_drug_name = Detect_closest_drug(user_input)
        if closest_drug_name:
            reply = gettinginfo(closest_drug_name)
        else:
            reply = "No matching drug found. Please check the spelling or try another drug name."

    return reply