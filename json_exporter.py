import json
from alien_species import AlienSpecies

class JsonExporter:
    """
    Handles converting a list of AlienSpecies objects back into a formatted JSON string 
    and writing it to a file. (This acts as the 'View' class).
    """
    
    def create_output_data(self, alien_list: list[AlienSpecies]) -> list[dict]:
        output_data = []
        for alien in alien_list:
            output_entry = {
                "id": alien.id,
                "name": alien.name,
                "universe": alien.classified_universe,
                "features": alien.features
            }
            output_data.append(output_entry)
        return output_data

    def write_to_file(self, data: list[dict], filename="classified_aliens_output.json"):
        try:
            json_string = json.dumps(data, indent=4)
            with open(filename, 'w') as f:
                f.write(json_string)
            print(f"✅ Success: Classified data written to '{filename}'")
        except Exception as e:
            print(f"❌ Error writing file: {e}")
