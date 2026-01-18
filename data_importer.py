import json
from alien_species import AlienSpecies

class DataImporter:
    """
    Handles reading the input file and converting the JSON content into AlienSpecies objects.
    """
    def read_json_file(self, filename="input.json"):
        try:
            with open(filename, 'r') as file:
                raw_data_string = file.read()
            parsed_data = json.loads(raw_data_string)
            print(f"✅ Successfully read and parsed {len(parsed_data)} entries from {filename}.")
            return parsed_data
        except FileNotFoundError:
            print(f"❌ ERROR: File '{filename}' not found. Please create it.")
            return []
        except json.JSONDecodeError:
            print(f"❌ ERROR: Could not parse JSON data in '{filename}'. Check file format.")
            return []

    def load_to_classes(self, filename="input.json"):
        raw_data = self.read_json_file(filename)
        alien_list = []
        for entry in raw_data:
            alien = AlienSpecies(
                id=entry['id'],
                name=entry['name'],
                features=entry['features']
            )
            alien_list.append(alien)
        print(f"✅ Successfully converted {len(alien_list)} entries into AlienSpecies objects.")
        return alien_list
