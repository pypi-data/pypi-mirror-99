import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gmshgeometry", # 폴더명과 동일한 이름
    version="0.0.7",
    author="CM2Lab",
    author_email="s.park@openest.eu",
    description="gmsh-based geometry controller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cm2lab/geodata_module",
    # ⬇︎ 배포하는 패키지의 다운로드 url을 적어줍니다.
    # ex_ download_url='https://github.com/doorBW/pypi_deploy_test/archive/master.zip',
    download_url='',
    # ⬇︎ 해당 패키지를 사용하기 위해 필요한 패키지를 적어줍니다. ex. install_requires= ['numpy', 'django']
    # 여기에 적어준 패키지는 현재 패키지를 install할때 함께 install됩니다.
    install_requires=[],
    packages=setuptools.find_packages(),
    # 패키지의 키워드를 적습니다.
    keywords=['gmsh geometry'],
    # ⬇︎ 파이썬 파일이 아닌 다른 파일을 포함시키고 싶다면 package_data에 포함시켜야 합니다.
    # ex) package_data= {'pyquibase' : ['db-connectors/sqlite-jdbc-3.18.0.jar', 'db-connectors/mysql-connector-java-5.1.42-bin.jar', 'liquibase/liquibase.jar' ]},
    package_data= {},
    # ⬇︎ 위의 package_data에 대한 설정을 하였다면 zip_safe설정도 해주어야 합니다. package_data가 있다면 zip_safe는 반드시 False로.
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)