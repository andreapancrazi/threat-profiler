import json
import requests

def get_groups_by_keyword(keyword):
    # URL of the enterprise-attack.json file
    url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    
    # Fetch the data from the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    data = response.json()
    
    # Filter groups by keyword in description
    groups = []
    for obj in data['objects']:
        if obj['type'] == 'intrusion-set' and 'description' in obj:
            if keyword.lower() in obj['description'].lower():
                groups.append(obj)
    
    return groups

def main(keyword):
    groups = get_groups_by_keyword(keyword)
    
    # Print the retrieved groups
    for group in groups:
        print(f"Name: {group['name']}")
        print(f"ID: {group['id']}")
        print(f"Description: {group['description']}\n")
    
    # Save the groups to a file
    with open(f'{keyword}_filtered_groups.json', 'w') as f:
        json.dump(groups, f, indent=4)
    
    print(f"Found {len(groups)} groups matching the keyword '{keyword}'. Results saved to '{keyword}_filtered_groups.json'.")

if __name__ == "__main__":
    keyword = input("Enter the keyword to filter groups by: ").strip()
    main(keyword)