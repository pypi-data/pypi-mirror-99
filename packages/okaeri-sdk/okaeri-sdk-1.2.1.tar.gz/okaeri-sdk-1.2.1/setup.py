from setuptools import setup, find_packages

setup(
    name='okaeri-sdk',
    url='https://github.com/OkaeriPoland/okaeri-sdk-python',
    author='Dawid Sawicki',
    author_email='dawid@okaeri.eu',
    install_requires=['requests', 'marshmallow-dataclass'],
    version='1.2.1',
    license='MIT',
    description='Okaeri Services SDK',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
