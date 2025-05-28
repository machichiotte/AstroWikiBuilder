# src/generate_star_drafts_main.py
import logging
import os

from src.models.star import Star, DataPoint
from src.utils.draft_utils import generate_star_draft, save_star_drafts


def main():
    """
    Main function to generate and save star article drafts.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)

    logger.info("Starting star draft generation process...")

    # 1. Create sample star data
    sample_stars = []

    sirius_data = {
        "name": DataPoint("Sirius"),
        "image": DataPoint("Sirius_A_and_B_artwork.jpg"),
        "caption": DataPoint("Artistic impression of Sirius A and B"),
        "epoch": DataPoint("J2000.0"),
        "right_ascension": DataPoint("06h 45m 08.9173s"),
        "declination": DataPoint("-16° 42′ 58.017″"),
        "constellation": DataPoint("Grand Chien"),
        "apparent_magnitude": DataPoint("-1.46"),
        "spectral_type": DataPoint("A1V + DA2"),
        "distance": DataPoint(value=2.64, unit="pc"),
        "mass": DataPoint(value=2.063, unit="M☉"),
        "radius": DataPoint(value=1.711, unit="R☉"),
        "temperature": DataPoint(value=9940, unit="K"),
        "age": DataPoint(value="237–247", unit="Myr"),
        "designations": DataPoint(
            ["Alpha Canis Majoris", "α CMa", "HD 48915", "HR 2491"]
        ),
    }
    sirius = Star(**sirius_data)
    sample_stars.append(sirius)

    proxima_data = {
        "name": DataPoint("Proxima Centauri"),
        "epoch": DataPoint("J2000.0"),
        "constellation": DataPoint("Centaure"),
        "distance": DataPoint(value=1.30197, unit="pc"),
        "spectral_type": DataPoint("M5.5Ve"),
        "apparent_magnitude": DataPoint("11.13"),
        "mass": DataPoint(value=0.1221, unit="M☉"),
        "radius": DataPoint(value=0.1542, unit="R☉"),
        "temperature": DataPoint(value=3042, unit="K"),
        "age": DataPoint(value="4.85", unit="Gyr"),
        "designations": DataPoint(
            "V645 Cen, Alpha Centauri C, HIP 70890"
        ),  # String, Star.__post_init__ handles it
    }
    proxima = Star(**proxima_data)
    sample_stars.append(proxima)

    sun_data = {
        "name": DataPoint("Sun"),
        "spectral_type": DataPoint("G2V"),
        "distance": DataPoint(
            value=1.0, unit="AU (distance from Earth)"
        ),  # Illustrative, not standard infobox distance
        "mass": DataPoint(value=1.0, unit="M☉"),
        "radius": DataPoint(value=1.0, unit="R☉"),
        "temperature": DataPoint(value=5778, unit="K"),
        "age": DataPoint(value="4.6", unit="Gyr"),
        "designations": DataPoint(["Sol", "Hélios"]),
    }
    sun = Star(**sun_data)
    sample_stars.append(sun)

    logger.info(f"Created {len(sample_stars)} sample star objects.")

    # 2. Generate drafts
    star_drafts_to_save = []
    for star_obj in sample_stars:
        star_name = (
            star_obj.name.value
            if star_obj.name and hasattr(star_obj.name, "value")
            else "UnknownStar"
        )
        logger.info(f"Generating draft for: {star_name}...")
        try:
            draft_content = generate_star_draft(star_obj)
            star_drafts_to_save.append((star_name, draft_content))
            logger.info(f"Draft generated successfully for {star_name}.")
        except Exception as e:
            logger.error(f"Error generating draft for {star_name}: {e}", exc_info=True)

    # 3. Save drafts
    if star_drafts_to_save:
        drafts_dir = "drafts/star"  # As per save_star_drafts default
        logger.info(f"Saving {len(star_drafts_to_save)} star drafts...")
        save_star_drafts(missing_drafts=star_drafts_to_save, existing_drafts=[])
        # The actual path is drafts/star/missing as per save_star_drafts implementation
        full_drafts_path = os.path.join(drafts_dir, "star_missing")
        logger.info(
            f"Star draft generation complete. Drafts saved in '{os.path.abspath(full_drafts_path)}'."
        )
    else:
        logger.info("No star drafts were generated to save.")


if __name__ == "__main__":
    main()
