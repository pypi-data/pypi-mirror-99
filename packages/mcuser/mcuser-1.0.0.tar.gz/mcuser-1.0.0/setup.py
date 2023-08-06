import setuptools

setuptools.setup(
    name="mcuser",
    version="1.0.0",
    license='MIT',
    author="babihoba",
    author_email="hobabot@gmail.com",
    description="Module for parsing Minecraft playerdb.co",
    long_description=open('README.md').read(),
    url="https://github.com/8954sood",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)