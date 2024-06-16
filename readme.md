## Threat Profiler

Threat Profiler is an open-source tool designed to streamline the process of threat profiling and gap assessment using the MITRE ATT&CK framework. This tool automates the steps of identifying relevant threat actors, downloading threat group layers, combining these layers, building mitigations layers based on techniques used by threat actors, and prioritizing mitigations to ensure comprehensive cybersecurity coverage.

### Features

1. Searching for threat actors by keyword (e.g., sector).
2. Downloading threat group layers.
3. Combining these layers to form a comprehensive threat landscape.
4. Building a mitigations layer based on the techniques used by identified threat actors in the combined layers.
5. Prioritizing these mitigations to ensure the most critical areas are addressed first. The priority of each mitigation is calculated as follows:

Priority of a Mitigation MI = (Number of occurrences of mitigation MI among techniques present in the layer) × (Weight of the techniques mitigated by MI)

### Installation

Clone the Repository:
```sh
git clone https://github.com/yourusername/threat-profiler.git
cd threat-profiler
```

Install Dependencies:

```sh
pip install -r requirements.txt
```

### Usage

```sh
$ python3 main.py -h                                                                                                                                                                  usage: main.py [-h] [--get-groups] [--download-layers] [--combine-layers] [--build-mitigations] [--calculate-occurences] [--calculate-priority] [--run-all] keyword                                                                     
                                                                                                                                                                                                                                        
Threat Profiler: Manipulate MITRE ATT&CK navigator layers                                                                                                                                                                            

positional arguments:
  keyword               The keyword to filter groups by

options:
  -h, --help            show this help message and exit
  --get-groups          Get groups by keyword
  --download-layers     Download group layers of <keyword_filtered_groups.json>
  --combine-layers      Combine group layers of <keyword_combined_groups_layer.json>
  --build-mitigations   Build mitigations layer based on <keyword_combined_groups_layer.json>
  --calculate-occurences
                        Calculate mitigations occurrences from combined attack layer file <keyword_combined_groups_layer.json>
  --calculate-priority  Calculate mitigations priority from combined attack layer file <keyword_combined_groups_layer.json>
  --run-all             Run all steps consecutively
```

Example of Complete Workflow:

1. Search for threat actors targeting a specific sector, for example:

```
python3 main.py --get-groups aviation
```

2. Download layers for the identified threat groups:

```
python3 main.py --download-layers aviation
```

3. Combine the downloaded layers into one consolidated comprehensive threat landscape layer:

```
python3 main.py --combine-layers aviation
```

4. Building a mitigations layer based on the techniques used by identified threat actors in the combined layers:

```
python3 main.py --build-mitigations aviation
```

5. Calculate Occurences of Mitigations:

```
python3 main.py --calculate-occurences aviation
```

6. Calculate Priority of Mitigations:

```
python3 main.py --calculate-priority aviation
```

or you can just run everything in one command:  

```
python3 main.py --run-all aviation
```

### Contributing

I welcome contributions to Threat Profiler! If you have suggestions for improvements, please open an issue or submit a pull request.

### License

Threat Profiler is licensed under the MIT License. See the LICENSE file for more information.

Thank you for using Threat Profiler! Your contributions and feedback are greatly appreciated.
