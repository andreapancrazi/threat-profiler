import json
import requests
from bs4 import BeautifulSoup

def load_combined_layer(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_mitigations_for_technique(technique_id):
    # URL of the MITRE ATT&CK website
    base_url = "https://attack.mitre.org/techniques/"
    url = f"{base_url}{technique_id}/"

    # If it's a subtechnique, adjust the URL format
    if "." in technique_id:
        technique_id_parts = technique_id.split(".")
        url = f"{base_url}{technique_id_parts[0]}/{technique_id_parts[1]}/"

    try:
        # Send a GET request to the technique's URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section containing mitigations
        mitigations_section = soup.find("h2", id="mitigations")
        if mitigations_section:
            # Find the parent div of the mitigations section
            parent_div = mitigations_section.find_next("div", class_="tables-mobile")

            # Find all table rows within the parent div
            mitigations_rows = parent_div.find_all("tr")

            # Extract the mitigations from the table rows
            mitigations_list = []
            for row in mitigations_rows:
                # Extract the table data from each row
                cols = row.find_all("td")
                if len(cols) >= 3:  # Ensure there are enough columns
                    mitigation_id = cols[0].get_text(strip=True)
                    # Check if the ID starts with "M" (indicating a mitigation)
                    if mitigation_id.startswith("M"):
                        mitigation_name = cols[1].get_text(strip=True)
                        mitigation_description = cols[2].get_text(strip=True)
                        mitigations_list.append({"ID": mitigation_id, "Mitigation": mitigation_name, "Description": mitigation_description})
            
            return mitigations_list
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []


def get_mitigations_for_combined_layer(combined_layer):
    techniques = combined_layer.get("techniques", [])
    mitigations_count = {}

    for technique in techniques:
        technique_id = technique.get("techniqueID")
        score = technique.get("score", 0)
        
        if score > 0:
            mitigations = get_mitigations_for_technique(technique_id)
            for mitigation in mitigations:
                mitigation_id = mitigation["ID"]
                if mitigation_id in mitigations_count:
                    mitigations_count[mitigation_id] += 1
                else:
                    mitigations_count[mitigation_id] = 1
    
    return mitigations_count

def main(combined_layer_filename):
    combined_layer = load_combined_layer(combined_layer_filename)
    
    if combined_layer:
        mitigations_count = get_mitigations_for_combined_layer(combined_layer)
        
        if mitigations_count:
            print("Mitigations found for techniques with score > 0 in the combined layer:")
            sorted_mitigations = sorted(mitigations_count.items(), key=lambda x: x[1], reverse=True)
            with open("mitigations_occurences.txt", "w") as f:
                for mitigation_id, count in sorted_mitigations:
                    f.write(f"ID: {mitigation_id}, Occurrences: {count}\n")
                    print(f"ID: {mitigation_id}, Occurrences: {count}")
        else:
            print("No mitigations found for techniques with score > 0 in the combined layer")
    else:
        print("Error loading the combined layer JSON file.")

if __name__ == "__main__":
    combined_layer_filename = input("Enter the filename of the combined layer JSON: ").strip()
    main(combined_layer_filename)
