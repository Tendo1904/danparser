from bs4 import BeautifulSoup, _typing
import shutil
import requests
from pathlib import Path
import time

class ImageParser(object):

    def __init__(self, 
                 url: str, 
                 character_name: str, 
                 output_size: int,
                 parsed_images: int = 0,
                 page_num: int = 1):
        self.url = url
        self.output_size = output_size
        self.name = character_name.lower().replace(" ", "_")
        self.output_dir = Path(Path(__file__).parent.parent/self.name)
        self.parsed_images = parsed_images
        self.page_num = page_num
        Path(self.output_dir).mkdir(exist_ok=True)

    @staticmethod
    def _get_page(request_url: str) -> requests.Response:
        return requests.get(request_url)
    
    def parse(self):
        while self.parsed_images < self.output_size:
            request_url = self._form_request()
            content = self._get_page(request_url).content
            time.sleep(0.1)
            soup = BeautifulSoup(content, "html.parser")
            image_list = soup.find_all('img', class_="post-preview-image")
            links_list = self._get_links(image_list)
            if self.parsed_images + len(links_list) > self.output_size:
                self._get_images(links_list[:self.output_size - self.parsed_images])
                self.parsed_images += (self.output_size - self.parsed_images)
            else:
                self._get_images(links_list)
                self.parsed_images += len(links_list)
            self.page_num += 1
        return self._get_links(image_list)

    def _form_request(self):
        return f"{self.url}/posts?page={str(self.page_num)}&tags={self.name}"
    
    @staticmethod
    def _get_links(image_list: _typing._QueryResults) -> list[str]:
        return [i.attrs['src'].replace("180x180", "original") for i in image_list]
    
    def _get_images(self, links_list: list[str]):
        for i, image in enumerate(links_list, 1 + self.parsed_images):
            image = self._check_response_code(image)
            response = requests.get(image, stream=True)
            time.sleep(0.1)
            with open(str(self.output_dir) + "/" + str(i) + image[-4:], "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
    
    @staticmethod
    def _check_response_code(img: str) -> str:
        if requests.get(img).status_code == 404:
            time.sleep(0.1)
            png_image = img.split(".jpg")[0] + ".png"
            if requests.get(png_image).status_code == 200:
                time.sleep(0.1)
                img = img.replace(".jpg", ".png")
        return img