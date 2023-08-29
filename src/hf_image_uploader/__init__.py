__version__ = "0.0.1"

import os
from huggingface_hub import HfApi
import tempfile
from typing import Optional, Union

api = HfApi()

def upload(image: Optional["PIL.Image"], repo_id: str, image_path: Optional[Union[str, os.PathLike]] = None, token: Optional[str] = None, repo_type: str = "dataset"):

    assert not isinstance(image, (tuple, list)), "Make sure that `image` is a single image instead of a list"

    if image is None and image_path is None:
        raise ValueError("Either `image` or `image_path` has to be defined.")

    temp_dir = None
    if image_path is None:
        temp_dir = tempfile.TemporaryDirectory()
        image_path = temp_dir.name + '/image.png'

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
