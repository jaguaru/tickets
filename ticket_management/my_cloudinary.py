from dotenv import dotenv_values
get_env_var = dotenv_values()

from io import BytesIO

from celery import shared_task

import cloudinary

cloudinary.config( 
    cloud_name = get_env_var['CLOUD_NAME'],
    api_key = get_env_var['API_KEY'],
    api_secret = get_env_var['API_SECRET'],
    # secure = get_env_var['SECURE']
)

import cloudinary.uploader
import cloudinary.api


@shared_task
def save_cloud_image(image_bytes):
    try:
        with BytesIO(image_bytes) as image_file:
            return cloudinary.uploader.upload(image_file)

    except Exception as _except:
        return str(_except)


@shared_task
def save_cloud_image_wait(image_file):
    cloud_image_saved = save_cloud_image.apply_async(args=[image_file])
    return cloud_image_saved.wait()
