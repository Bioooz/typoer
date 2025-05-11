from setuptools import setup, find_packages

setup(
    name="typoer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "keyboard>=0.13.5",
        "transformers==4.36.2",
        "torch==2.1.2",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "google-generativeai>=0.3.0",
    ],
    entry_points={
        'console_scripts': [
            'typoer=typoer.cli:main',
            'typoer-gui=typoer.gui:main',
        ],
    },
    author="Bioooz",
    author_email="sae.arefazimi@gmail.com",
    description="A tool that simulates human typing with realistic typos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Bioooz/typoer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 