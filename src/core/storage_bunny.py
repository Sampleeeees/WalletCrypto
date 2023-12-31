import base64
import os
import random
import string

from BunnyCDN.Storage import Storage
from BunnyCDN.CDN import CDN

class BunnyStorage:
    """ Клас за допомогою якого буде відправлятися фото на storage bunny"""
    def __init__(self, api_key: str, storage_name: str, storage_region: str):
        self.api_key = api_key
        self.storage_name = storage_name
        self.storage_region = storage_region
        self.cdn_path = ''

    # Отримання storage через api_key
    async def get_storage(self) -> Storage:
        return Storage(api_key=self.api_key, storage_zone=self.storage_name)

    async def get_cdn(self) -> CDN:
        return CDN(api_key=self.api_key)

    # створення рандомної назви картинки
    async def generate_random_filename(self, length: int = 10) -> str:
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    # перетворення картинки з base64 на звичайну та відправка на bunny storage
    async def upload_image_to_bunny(self, base64photo):

        base64_data = base64photo.split(',', 1)[1] # Видалення префіксу)

        format_start = base64photo.find('/') + 1 # Початок формату файлу
        format_end = base64photo.find(';', format_start) # Закінчення формату файлу

        file_format = base64photo[format_start: format_end] # Отримання назви формату файлу

        image_data = base64.b64decode(base64_data) # перетворення картинки на image
        filename = await self.generate_random_filename() + f'.{file_format}' # генерація рандомної назви картинки

        with open(filename, 'wb') as f:
            f.write(image_data)

        storage = await self.get_storage() # отримання storage

        storage.PutFile(file_name=filename) # відправка фото на bunny.net

        url = f'https://cryptowallet.b-cdn.net/{filename}' # Отримання url картинки для збереження в базу даних
        print(url)

        os.remove(filename) # видалення фото з локального коду

        return url

    # Видалення фото коли користувач його хоче змінити
    async def delete_photo(self, url_photo) -> None:
        filename = url_photo.split('/')[-1] # Отримання назви з url

        storage = await self.get_storage() # Ініціалізація стораджу
        storage.DeleteFile(filename) # Видалення фото з bunny.net

