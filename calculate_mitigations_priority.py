import json
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def load_combined_layer(filename):
    with open(filename, 'r') as f:
        return json.load(f)

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

def get_mitigations_for_combined_layer(combined_layer):
    techniques = combined_layer.get("techniques", [])
    mitigations_info = defaultdict(lambda: {"count": 0, "techniques": [], "priority": 0})

    for technique in techniques:
        technique_id = technique.get("techniqueID")
        score = technique.get("score", 0)
        
        if score > 0:
            mitigations = get_mitigations_for_technique(technique_id)
            for mitigation in mitigations:
                mitigation_id = mitigation["ID"]
                mitigations_info[mitigation_id]["count"] += 1
                mitigations_info[mitigation_id]["techniques"].append({
                    "techniqueID": technique_id, 
                    "score": score
                })
                mitigations_info[mitigation_id]["priority"] += score
    
    return mitigations_info

def main(combined_layer_filename):
    combined_layer = load_combined_layer(combined_layer_filename)
    
    if combined_layer:
        mitigations_info = get_mitigations_for_combined_layer(combined_layer)
        
        if mitigations_info:
            print("Mitigations found for techniques with score > 0 in the combined layer:")
            sorted_mitigations = sorted(mitigations_info.items(), key=lambda x: x[1]["priority"], reverse=True)
            with open("mitigations_details.txt", "w") as f:
                f.write("Mitigation ID,Occurrences,Techniques,Priority\n")
                for mitigation_id, info in sorted_mitigations:
                    techniques_str = "; ".join([f"{t['techniqueID']} (score: {t['score']})" for t in info["techniques"]])
                    line = f"{mitigation_id},{info['count']},{techniques_str},{info['priority']}\n"
                    f.write(line)
                    print(f"Mitigation ID: {mitigation_id}, Occurrences: {info['count']}, Priority: {info['priority']}")
                    print(f"  Techniques: {techniques_str}")
        else:
            print("No mitigations found for techniques with score > 0 in the combined layer")
    else:
        print("Error loading the combined layer JSON file.")

if __name__ == "__main__":
    combined_layer_filename = input("Enter the filename of the combined layer JSON: ").strip()
    main(combined_layer_filename)
