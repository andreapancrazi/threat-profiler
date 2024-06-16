import json
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def get_mitigations_for_technique(technique_id):
    base_url = "https://attack.mitre.org/techniques/"
    url = f"{base_url}{technique_id}/"
    if "." in technique_id:
        technique_id_parts = technique_id.split(".")
        url = f"{base_url}{technique_id_parts[0]}/{technique_id_parts[1]}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        mitigations_section = soup.find("h2", id="mitigations")
        if mitigations_section:
            parent_div = mitigations_section.find_next("div", class_="tables-mobile")
            mitigations_rows = parent_div.find_all("tr")
            mitigations_list = []
            for row in mitigations_rows:
                cols = row.find_all("td")
                if len(cols) >= 3:
                    mitigation_id = cols[0].get_text(strip=True)
                    if mitigation_id.startswith("M"):
                        mitigation_name = cols[1].get_text(strip=True)
                        mitigation_description = cols[2].get_text(strip=True)
                        mitigations_list.append({
                            "ID": mitigation_id, 
                            "Mitigation": mitigation_name, 
                            "Description": mitigation_description
                        })
            return mitigations_list
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def load_layer(layer_path):
    with open(layer_path, 'r') as file:
        return json.load(file)

def combine_layers(layers_directory, keyword):
    combined_layer = {
        "name": f"mitigations for {keyword} threat groups",
        "description": f"Combination of all mitigations layers for {keyword} threat groups",
        "versions": {
            "attack": "15",
            "navigator": "5.0.1",
            "layer": "4.5"
        },
        "domain": "enterprise-attack",
        "techniques": [],
        "gradient": {
            "colors": ["#ffffff00", "#0000ffff"],
            "minValue": 1,
            "maxValue": 1  # Placeholder value, will be updated later
        },
        "layout": {
            "layout": "side",
            "aggregateFunction": "average",
            "showID": False,
            "showName": True,
            "showAggregateScores": True,
            "countUnscored": False,
            "expandedSubtechniques": "none"
        },
        "hideDisabled": False
    }
    
    techniques_dict = defaultdict(float)
    num_layers = 0
    
    for layer_file in os.listdir(layers_directory):
        if layer_file.endswith('.json'):
            num_layers += 1
            layer_path = os.path.join(layers_directory, layer_file)
            layer = load_layer(layer_path)
            for technique in layer.get('techniques', []):
                technique_id = technique.get('techniqueID')
                score = technique.get('score', 0)
                if technique_id and score > 0:
                    techniques_dict[technique_id] += score
    
    max_value = max(techniques_dict.values(), default=1)
    
    combined_layer['gradient']['maxValue'] = max_value
    
    for technique_id, score in techniques_dict.items():
        combined_layer['techniques'].append({
            "techniqueID": technique_id,
            "score": score,
            "color": ""
        })

    return combined_layer

def download_mitigation_layer(mitigation_id, layers_directory):
    url = f"https://attack.mitre.org/mitigations/{mitigation_id}/{mitigation_id}-enterprise-layer.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        layer_path = os.path.join(layers_directory, f"{mitigation_id}.json")
        with open(layer_path, 'w') as file:
            file.write(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")

def main(keyword):
    combined_layer_file = f"{keyword}_combined_groups_layer.json"
    layers_directory = f"{keyword}-mitigations-layers"
    os.makedirs(layers_directory, exist_ok=True)

    with open(combined_layer_file, 'r') as f:
        combined_layer = json.load(f)

    for technique in combined_layer.get('techniques', []):
        if technique.get('score', 0) > 0:
            technique_id = technique['techniqueID']
            mitigations = get_mitigations_for_technique(technique_id)
            for mitigation in mitigations:
                mitigation_id = mitigation['ID']
                download_mitigation_layer(mitigation_id, layers_directory)

    combined_mitigation_layer = combine_layers(layers_directory, keyword)
    
    output_filename = f"{keyword}_combined_mitigations_layer.json"
    with open(output_filename, "w") as file:
        json.dump(combined_mitigation_layer, file, indent=4)
    
    print(f"Output saved to {output_filename}")

if __name__ == "__main__":
    keyword = input("Enter the keyword to filter by: ").strip()
    main(keyword)
