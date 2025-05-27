import re

def parse_categories(file_path="notes/categories_notes.md"):
    """
    Parses a markdown file to extract categories.

    Args:
        file_path (str): The path to the markdown file.

    Returns:
        dict: A dictionary where keys are category types and
              values are lists of category names.
    """
    categories = {}
    current_category_type = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Check for category type headers
            if not line.startswith("[["):
                current_category_type = line
                if "Discovery Years" in current_category_type:
                    # Extract years from "Discovery Years (from YYYY to YYYY)"
                    match = re.search(r'\(from (\d{4}) to (\d{4})\)', current_category_type)
                    if match:
                        start_year, end_year = int(match.group(1)), int(match.group(2))
                        categories[current_category_type] = [
                            f"[[Catégorie:Exoplanète découverte en {year}]]"
                            for year in range(start_year, end_year + 1)
                        ]
                    else:
                        # Fallback or error if format is unexpected
                        categories[current_category_type] = []
                else:
                    categories[current_category_type] = []
            elif current_category_type and line.startswith("[[Catégorie:") and "Discovery Years" not in current_category_type:
                # Add category items to the current type, if not a special case like Discovery Years
                categories[current_category_type].append(line)
            # Lines for "Discovery Years" are generated and should not be appended here from the file
            # if "Discovery Years" in current_category_type and line.startswith("[[Catégorie:"):
            #    pass # Already handled by year range generation

    return categories

if __name__ == '__main__':
    # Example usage:
    parsed_cats = parse_categories()
    for cat_type, cat_list in parsed_cats.items():
        print(f"Category Type: {cat_type}")
        for cat_name in cat_list:
            print(f"  - {cat_name}")
        print("-" * 20)
    
    # Verify specific handling for Discovery Years
    if "Discovery Years (from 1992 to 2025)" in parsed_cats:
        print("Verifying Discovery Years:")
        expected_first_year = "[[Catégorie:Exoplanète découverte en 1992]]"
        expected_last_year = "[[Catégorie:Exoplanète découverte en 2025]]"
        if parsed_cats["Discovery Years (from 1992 to 2025)"][0] == expected_first_year and \
           parsed_cats["Discovery Years (from 1992 to 2025)"][-1] == expected_last_year and \
           len(parsed_cats["Discovery Years (from 1992 to 2025)"]) == (2025 - 1992 + 1):
            print("Discovery Years generated correctly.")
        else:
            print("Error in Discovery Years generation.")
            print(f"First: {parsed_cats['Discovery Years (from 1992 to 2025)'][0]}")
            print(f"Last: {parsed_cats['Discovery Years (from 1992 to 2025)'][-1]}")
            print(f"Count: {len(parsed_cats['Discovery Years (from 1992 to 2025)'])}")

    # Check if other categories are parsed
    if "Constellations" in parsed_cats and len(parsed_cats["Constellations"]) > 0:
        print("Constellations parsed.")
    else:
        print("Constellations not parsed or empty.")

    # Check for duplicated category types (they appear twice in the input file)
    # The current logic will overwrite the first instance with the second for "Discovery Instruments/Telescopes"
    # This is acceptable based on the problem description focusing on extraction, not merging duplicates.
    # However, if merging was required, the logic would need adjustment.
    print("Note: The input file contains 'Discovery Instruments/Telescopes' twice.")
    print("The parser will reflect the last encountered instance of a category type.")

    # Test with a non-existent file
    try:
        parse_categories("non_existent_file.md")
    except FileNotFoundError:
        print("Handled FileNotFoundError correctly.")
    except Exception as e:
        print(f"Unexpected error for non-existent file: {e}")
