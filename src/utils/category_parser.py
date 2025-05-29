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

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Check for category type headers
            if not line.startswith("[["):
                current_category_type = line
                if "Discovery Years" in current_category_type:
                    # Extract years from "Discovery Years (from YYYY to YYYY)"
                    match = re.search(
                        r"\(from (\d{4}) to (\d{4})\)", current_category_type
                    )
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
            elif (
                current_category_type
                and line.startswith("[[Catégorie:")
                and "Discovery Years" not in current_category_type
            ):
                # Add category items to the current type, if not a special case like Discovery Years
                categories[current_category_type].append(line)
            # Lines for "Discovery Years" are generated and should not be appended here from the file
            # if "Discovery Years" in current_category_type and line.startswith("[[Catégorie:"):
            #    pass # Already handled by year range generation

    return categories
