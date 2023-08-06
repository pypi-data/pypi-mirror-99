import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="autopayparking",
    description="Pay and automatically renew PayByPhone parking using CLI",
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1",
    py_modules=["autopayparking"],
    install_requires=[
        "click",
        "selenium",
    ],
    entry_points="""
        [console_scripts]
        autopayparking=autopayparking.autopay:cli
    """,
)
