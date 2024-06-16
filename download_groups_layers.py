import os
import json
import requests

def create_layers_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_group_layer(group, directory):
    group_name = group['name']
    
    # Find the URL and external_id from external_references
    mitre_reference = next((ref for ref in group.get('external_references', []) if ref['source_name'] == 'mitre-attack'), None)
    
    if mitre_reference:
        external_id = mitre_reference['external_id']
        layer_url = f"https://attack.mitre.org/groups/{external_id}/{external_id}-enterprise-layer.json"
        
        try:
            response = requests.get(layer_url)
            response.raise_for_status()
            
            # Save the layer to a file
            layer_filename = f"{directory}/{group_name.replace(' ', '_')}.json"
            layer_data = response.json()
            layer_data['versions']['layer'] = '4.5'  # Update layer version to 4.5
            with open(layer_filename, 'w') as layer_file:
                json.dump(layer_data, layer_file, indent=4)
            
            print(f"Layer for group '{group_name}' saved to {layer_filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download layer for group '{group_name}': {e}")
    else:
        print(f"No mitre-attack reference found for group '{group_name}'")

def main(keyword):
    input_filename = f"{keyword}_filtered_groups.json"
    layers_directory = f"{keyword}-group-layers"
    
    # Create layers directory if it doesn't exist
    create_layers_directory(layers_directory)
    
    # Read the filtered groups from the input file
    with open(input_filename, 'r') as f:
        groups = json.load(f)
    
    # Download and save the layer for each group
    for group in groups:
        download_group_layer(group, layers_directory)

if __name__ == "__main__":
    keyword = input("Enter the keyword to filter by: ").strip()
    main(keyword)