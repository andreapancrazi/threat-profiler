import os
import json

def load_layer(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def combine_layers(layers_directory, keyword):
    combined_layer = {
        "name": f"{keyword} threat groups",
        "description": f"Combination of all {keyword} threat groups layers",
        "versions": {
            "attack": "15",
            "navigator": "5.0.1",
            "layer": "4.5"
        },
        "domain": "enterprise-attack",
        "techniques": []
    }
    
    techniques_set = set()
    
    # Get the total number of layers
    num_layers = len([name for name in os.listdir(layers_directory) if name.endswith('.json')])
    
    # Set the color gradient from transparent to red with low value: 1 and high value: num_layers
    color_gradient = ["#ffffff00", "#ff6666ff"]
    
    # Iterate over all files in the layers directory
    for i, layer_file in enumerate(os.listdir(layers_directory)):
        if layer_file.endswith('.json'):
            layer_path = os.path.join(layers_directory, layer_file)
            layer = load_layer(layer_path)
            
            # Add techniques from the current layer to the combined layer
            for technique in layer.get('techniques', []):
                technique_id = technique.get('techniqueID')
                if technique_id and technique_id not in techniques_set:
                    techniques_set.add(technique_id)
                    technique['score'] = i + 1  # Set score from 1 to num_layers
                    technique['color'] = ""  # Reset color to use gradient
                    technique['comment'] = ""  # Remove comment
                    combined_layer['techniques'].append(technique)
    
    # Add gradient color settings
    combined_layer['gradient'] = {
        "colors": color_gradient,
        "minValue": 1,
        "maxValue": num_layers
    }
    
    # Add layout information
    combined_layer['layout'] = {
        "layout": "side",
        "aggregateFunction": "average",
        "showID": False,
        "showName": True,
        "showAggregateScores": True,  # Set to True to display aggregated scores
        "countUnscored": False,
        "expandedSubtechniques": "none"
    }
    
    return combined_layer

def main(keyword):
    layers_directory = f"{keyword}-group-layers"
    output_filename = f"{keyword}_combined_groups_layer.json"
    
    # Combine all layers
    combined_layer = combine_layers(layers_directory, keyword)
    
    # Save the combined layer to a file
    with open(output_filename, 'w') as f:
        json.dump(combined_layer, f, indent=4)
    
    print(f"Combined layer saved to {output_filename}")

if __name__ == "__main__":
    keyword = input("Enter the keyword to filter by: ").strip()
    main(keyword)
