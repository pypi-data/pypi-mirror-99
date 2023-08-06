from setuptools import setup, find_packages


setup(
    name="avilabs-snippets",
    version="0.0.1",
    description="Grab bag of useful snippets",
    author="Avilay Parekh",
    author_email="avilay@gmail.com",
    license="MIT",
    url="https://gitlab.com/avilay/snippets",
    packages=find_packages(),
    install_requires=["colorama", "termcolor", "psutil"],
)
