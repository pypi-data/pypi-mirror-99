import setuptools

name = "PikaTgBot"
author = "ItzSjDude"
author_email = "Support@ItzSjDude.in"
description = "A Secure and Optimized Python-Telethon Based Library For Pikachu UserBot aka Pikabot."
license = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
url = "https://github.com/ItzSjDude/PikachuUserbot"
requirements = list(map(str.strip, open("requirements.txt").readlines()))
setuptools.setup(
    name=name,
    version="1.3.93",
    author=author,
    author_email=author_email,
    description=description,
    url=url,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
