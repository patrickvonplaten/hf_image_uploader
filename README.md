# image_uploader

Use this package to have an easier way to upload images to the HF Hub when working on remote machines:
```bash
!pip install hf_image_uploader
```

Make sure to be logged in:
```
huggingface-cli login
```

Then it's a one-liner to upload an image to a repo.

```py
import hf_image_uploader as hfi

# ... run diffusers code
# image = pipe(...).images[0]

hfi.upload(image, repo_id="patrickvonplaten/images")
```
