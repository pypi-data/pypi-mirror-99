import setuptools

setuptools.setup(
    name="capybara-cophylogeny",
    version="0.0.7",
    author="Hélio Wang",
    author_email="helioaimelesoleil@gmail.com",
    description="Capybara Python package for phylogenetic tree reconciliation",
    long_description="""
    Use Capybara's counter and enumerator as Python modules!
    
    ## Documentation
    https://capybara-doc.readthedocs.io/en/latest
    """,
    long_description_content_type="text/markdown",
    url="https://github.com/Helio-Wang/Capybara-app",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

