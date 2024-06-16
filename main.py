import argparse
import get_groups_by_keyword
import download_groups_layers
import combine_groups_layers
import build_mitigations_layer
import calculate_mitigations_occurences
import calculate_mitigations_priority

def main():
    parser = argparse.ArgumentParser(description="Threat Profiler: Manipulate MITRE ATT&CK navigator layers")
    
    parser.add_argument("keyword", help="The keyword to filter groups by")
    
    parser.add_argument("--get-groups", action="store_true", help="Get groups by keyword")
    parser.add_argument("--download-layers", action="store_true", help="Download group layers of <keyword_filtered_groups.json>")
    parser.add_argument("--combine-layers", action="store_true", help="Combine group layers of <keyword_combined_groups_layer.json>")
    parser.add_argument("--build-mitigations", action="store_true", help="Build mitigations layer based on <keyword_combined_groups_layer.json>")
    
    parser.add_argument("--calculate-occurences", action="store_true", help="Calculate mitigations occurrences from combined attack layer file <keyword_combined_groups_layer.json>")
    parser.add_argument("--calculate-priority", action="store_true", help="Calculate mitigations priority from combined attack layer file <keyword_combined_groups_layer.json>")
    
    parser.add_argument("--run-all", action="store_true", help="Run all steps consecutively")
    
    args = parser.parse_args()
    
    def run_all(keyword):
        get_groups_by_keyword.main(keyword)
        download_groups_layers.main(keyword)
        combine_groups_layers.main(keyword)
        build_mitigations_layer.main(keyword)

        calculate_mitigations_occurences.main(combined_layer_filename)
        calculate_mitigations_priority.main(combined_layer_filename)
    
    combined_layer_filename = f"{args.keyword}_combined_groups_layer.json"
    
    if args.run_all:
        run_all(args.keyword)
    else:
        if args.get_groups:
            get_groups_by_keyword.main(args.keyword)
        
        if args.download_layers:
            download_groups_layers.main(args.keyword)
        
        if args.combine_layers:
            combine_groups_layers.main(args.keyword)
        
        if args.build_mitigations:
            build_mitigations_layer.main(args.keyword)
        
        if args.calculate_occurences:
            calculate_mitigations_occurences.main(combined_layer_filename)
        
        if args.calculate_priority:
            calculate_mitigations_priority.main(combined_layer_filename)
    
if __name__ == "__main__":
    main()