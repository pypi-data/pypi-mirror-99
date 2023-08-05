import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gmshgeometry", # 폴더명과 동일한 이름
    version="0.0.5",
    author="CM2Lab",
    author_email="s.park@openest.eu",
    description="gmsh-based geometry controller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cm2lab/geodata_module",
    # ⬇︎ 해당 패키지를 사용하기 위해 필요한 패키지를 적어줍니다. ex. install_requires= ['numpy', 'django']
    # 여기에 적어준 패키지는 현재 패키지를 install할때 함께 install됩니다.
    install_requires=[],
    packages=setuptools.find_packages(),
    # 패키지의 키워드를 적습니다.
    keywords=['gmsh geometry'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)