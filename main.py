# main.py
from data_importer import DataImporter
from classifier import Classifier
from json_exporter import JsonExporter

if __name__ == '__main__':
    # --- Day 3: Load Data ---
    importer = DataImporter()
    all_aliens = importer.load_to_classes() 
    
    # --- Day 4: Classify ---
    classifier = Classifier()
    print("\n--- Running Classification (Day 4) ---")
    for alien in all_aliens:
        classifier.classify_species(alien)
    
    # --- Day 5: Export Data ---
    exporter = JsonExporter()
    
    # 1. Convert the objects back into a list of dictionaries
    output_data_list = exporter.create_output_data(all_aliens)

    # 2. Write the resulting list to a file
    exporter.write_to_file(output_data_list)
    
    print("\nLab work completed. Ready for PR submission!")
