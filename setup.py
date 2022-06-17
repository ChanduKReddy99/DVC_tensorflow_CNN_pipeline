from setuptools import setup

with open("README.md", "r", encoding= 'utf-8') as fh:
    long_description = fh.read()

REPO_NAME = 'DVC_usecase_in_Tensorflow_CNN'
AUTHOR_USER_NAME = "ChanduKReddy99"
AUTHOR_EMAIL = "chanduk.amical@gmail.com"
URL="https://github.com/ChanduKReddy99/DVC_tensorflow_CNN"
SRC_REPO= 'src'
INSTALL_REQUIRES = [
    'dvc',
    'tensorflow',
    'pandas',
    'boto3',
]



setup(
    name=SRC_REPO,
    version='0.0.1',
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description='DVC usecase in Tensorflow CNN',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    packages=[SRC_REPO],
    license='MIT',
    python_requires='>=3.6',
    install_requires=INSTALL_REQUIRES

)

