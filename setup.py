# Copyright 2023 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Simple check list from AllenNLP repo: https://github.com/allenai/allennlp/blob/main/setup.py

To create the package for pypi.

1. Run `make pre-release` (or `make pre-patch` for a patch release) then run `make fix-copies` to fix the index of the
   documentation.

   If releasing on a special branch, copy the updated README.md on the main branch for your the commit you will make
   for the post-release and run `make fix-copies` on the main branch as well.

2. Run Tests for Amazon Sagemaker. The documentation is located in `./tests/sagemaker/README.md`, otherwise @philschmid.

3. Unpin specific versions from setup.py that use a git install.

4. Checkout the release branch (v<RELEASE>-release, for example v4.19-release), and commit these changes with the
   message: "Release: <RELEASE>" and push.

5. Wait for the tests on main to be completed and be green (otherwise revert and fix bugs)

6. Add a tag in git to mark the release: "git tag v<RELEASE> -m 'Adds tag v<RELEASE> for pypi' "
   Push the tag to git: git push --tags origin v<RELEASE>-release

7. Build both the sources and the wheel. Do not change anything in setup.py between
   creating the wheel and the source distribution (obviously).

   For the wheel, run: "python setup.py bdist_wheel" in the top level directory.
   (this will build a wheel for the python version you use to build it).

   For the sources, run: "python setup.py sdist"
   You should now have a /dist directory with both .whl and .tar.gz source versions.

   Long story cut short, you need to run both before you can upload the distribution to the 
   test pypi and the actual pypi servers: 
   
   python setup.py bdist_wheel && python setup.py sdist

8. Check that everything looks correct by uploading the package to the pypi test server:

   twine upload dist/* -r pypitest
   (pypi suggest using twine as other methods upload files via plaintext.)
   You may have to specify the repository url, use the following command then:
   twine upload dist/* -r pypitest --repository-url=https://test.pypi.org/legacy/

   Check that you can install it in a virtualenv by running:
   pip install -i https://testpypi.python.org/pypi diffusers

   If you are testing from a Colab Notebook, for instance, then do:
   pip install diffusers && pip uninstall diffusers
   pip install -i https://testpypi.python.org/pypi diffusers

   Check you can run the following commands:
   python -c "python -c "from diffusers import __version__; print(__version__)"
   python -c "from diffusers import DiffusionPipeline; pipe = DiffusionPipeline.from_pretrained('fusing/unet-ldm-dummy-update'); pipe()"
   python -c "from diffusers import DiffusionPipeline; pipe = DiffusionPipeline.from_pretrained('hf-internal-testing/tiny-stable-diffusion-pipe', safety_checker=None); pipe('ah suh du')"
   python -c "from diffusers import *"

9. Upload the final version to actual pypi:
   twine upload dist/* -r pypi

10. Prepare the release notes and publish them on github once everything is looking hunky-dory.

11. Run `make post-release` (or, for a patch release, `make post-patch`). If you were on a branch for the release,
    you need to go back to main before executing this.
"""
from setuptools import find_packages, setup


setup(
    name="hf_image_uploader",
    version="0.0.1",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
    description="State-of-the-art diffusion in PyTorch and JAX.",
    long_description="long",
    long_description_content_type="text/markdown",
    keywords="deep learning diffusion jax pytorch stable diffusion audioldm",
    license="Apache",
    author="The HuggingFace team",
    author_email="patrick@huggingface.co",
    url="https://github.com/patrickvonplaten/image_uploader",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    python_requires=">=3.7.0",
    install_requires=[
        "huggingface_hub"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)

# Release checklist
# 1. Change the version in __init__.py and setup.py.
# 2. Commit these changes with the message: "Release: Release"
# 3. Add a tag in git to mark the release: "git tag RELEASE -m 'Adds tag RELEASE for pypi' "
#    Push the tag to git: git push --tags origin main
# 4. Run the following commands in the top-level directory:
#      python setup.py bdist_wheel
#      python setup.py sdist
# 5. Upload the package to the pypi test server first:
#      twine upload dist/* -r pypitest
#      twine upload dist/* -r pypitest --repository-url=https://test.pypi.org/legacy/
# 6. Check that you can install it in a virtualenv by running:
#      pip install -i https://testpypi.python.org/pypi diffusers
#      diffusers env
#      diffusers test
# 7. Upload the final version to actual pypi:
#      twine upload dist/* -r pypi
# 8. Add release notes to the tag in github once everything is looking hunky-dory.
# 9. Update the version in __init__.py, setup.py to the new version "-dev" and push to master
