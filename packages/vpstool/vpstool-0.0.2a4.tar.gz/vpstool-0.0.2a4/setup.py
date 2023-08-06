import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vpstool",
    version="0.0.2a4",
    author="SLP",
    author_email="byteleap@gmail.com",
    description="VPS toolkits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/vpstool",
    packages=setuptools.find_packages(),
    package_data={'vps': ['a.out']},
    zip_safe=False,
    install_requires=[
        'colorlog>=4.6.1', 'tqdm', 'lxml', 'requests', 'dofast',
        'smart-open', 'pillow', 'bs4', 'arrow', 'numpy', 'termcolor', 'pycrytpo'
    ],
    entry_points={
        'console_scripts': ['tool=vps.argparse_helper:parse_arguments']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
