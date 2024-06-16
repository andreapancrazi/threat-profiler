import requests
from bs4 import BeautifulSoup

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

def main():
    technique_id = input("Enter the technique ID: ").strip()
    mitigations = get_mitigations_for_technique(technique_id)
    
    if mitigations:
        print(f"Mitigations for technique {technique_id}:")
        for mitigation in mitigations:
            print("ID:", mitigation["ID"])
            print("Mitigation:", mitigation["Mitigation"])
            print("Description:", mitigation["Description"])
            print()
    else:
        print(f"No mitigations found for technique {technique_id}")

if __name__ == "__main__":
    main()
