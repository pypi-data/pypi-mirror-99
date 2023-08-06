import setuptools

setuptools.setup(
    name="mcuser",
    version="1.0.1",
    license='MIT',
    author="babihoba",
    author_email="hobabot@gmail.com",
    description="parsing for Minecraft User Data module",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/8954sood/mcuser",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)