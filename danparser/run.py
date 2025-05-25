from parsers import ImageParser
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(message)s"
)

if __name__ == "__main__":
    url = "https://danbooru.donmai.us"
    name = "Astolfo (Fate)"
    size = 100
    parser = ImageParser(url=url,
                         character_name=name,
                         output_size=size)
    logging.info(f"output dir: {parser.output_dir}")
    logging.info(f"Processing url: {parser.url}\nRequested character: {parser.name}\n")
    while True:
        try:
            logging.info(f"Pictures on the 1st page: {parser.parse()}")
            break
        except Exception as e:
            logging.info(f"Faced exception {e} on page {parser.page_num}")
            logging.info(f"Trying to continue parsing ...")
            pass
