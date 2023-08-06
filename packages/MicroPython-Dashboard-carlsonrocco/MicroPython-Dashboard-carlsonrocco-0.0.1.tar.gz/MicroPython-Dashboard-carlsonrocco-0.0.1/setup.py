import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MicroPython-Dashboard-carlsonrocco", # Replace with your own username
    version="0.0.1",
    author="Rocco Carlson",
    author_email="rocstrrr@gmail.com",
    description="A modular dashboard made using WS2812b individually addressable LEDs and an ESP8266 microcontroller running MicroPython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['dashboard'],
    python_requires=">=3.6",
)