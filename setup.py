from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='superannotate_schemas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0',
    package_dir={"": "src"},
    description='SuperAnnotate JSON Schemas',
    author='Vaghinak Basentsyan',
    author_email='vaghinak@superannotate.con',
    url='https://www.superannotate.com/',
    license='MIT',
    description_file="README.md",
    entry_points={
            'console_scripts': ['superannotate_schemas = bin.app:main']
        },
      )
