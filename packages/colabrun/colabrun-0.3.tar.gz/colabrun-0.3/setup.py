import setuptools

setuptools.setup(
    name='colabrun',
    version='0.3',
    author="hoa",
    author_email="getmoneykhmt3@gmail.com",
    description="A Des of sreup",
    long_description="colabrun",
    long_description_content_type="text/markdown",
    url="https://github.com/vtandroid/colabrun",
    packages=setuptools.find_packages(),
    py_modules=['colabrun'],
    install_requires=[
        'selenium','requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )