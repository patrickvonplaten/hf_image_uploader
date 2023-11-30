__version__ = "0.0.2"

import os
from huggingface_hub import HfApi
import tempfile
from typing import Optional, Union
import random
import string

api = HfApi()


def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # Includes both letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def upload(image: Optional["PIL.Image"] = None, repo_id: Optional[str] = None, image_path: Optional[Union[str, os.PathLike]] = None, name: Optional[str] = None, token: Optional[str] = None, repo_type: str = "dataset"):

    assert not isinstance(image, (tuple, list)), "Make sure that `image` is a single image instead of a list"

    if image is None and image_path is None:
        raise ValueError("Either `image` or `image_path` has to be defined.")

    name = name or f"{generate_random_string(10)}.png"

    temp_dir = None
    if image_path is None:
        temp_dir = tempfile.TemporaryDirectory()
        image_path = os.path.join(temp_dir.name, name)

    if not os.path.exists(image_path):
        image.save(image_path)

    path_in_repo = image_path.split("/")[-1]

    api.upload_file(
        path_or_fileobj=image_path,
        path_in_repo=path_in_repo,
        repo_id=repo_id,
        token=token,
        repo_type=repo_type,
    )
    repo_type = f"/{repo_type}s" if repo_type != "model" else ""
    print(f"https://huggingface.co{repo_type}/{repo_id}/blob/main/{path_in_repo}")

    if temp_dir is not None:
        temp_dir.cleanup() 
