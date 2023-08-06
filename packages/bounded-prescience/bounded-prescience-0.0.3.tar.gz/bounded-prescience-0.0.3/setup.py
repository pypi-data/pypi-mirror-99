import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bounded-prescience',
    version='0.0.3',
    author="Hjalmar Wijk, Hosein Hasanbeig, Mirco Giacobbe, Daniel Kroening",
    author_email="hjalmar.wijk@gmail.com, hosein.hasanbeig@icloud.com",
    keywords='rl, safety, atari, agent',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/HjalmarWijk/bounded-prescience',
    description='Shielding Atari Games with Bounded Prescience',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        'chainer',
        'chainerrl',
        'numpy',
        'Pillow',
        'gym',
        'gym[atari]',
        'cmake',
        'opencv-python',
        'tensorflow'
    ]
)