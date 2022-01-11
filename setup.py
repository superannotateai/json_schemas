from pathlib import Path
from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='superannotate_schemas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0.0b3',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    description='SuperAnnotate JSON Schemas',
    author='Vaghinak Basentsyan',
    author_email='vaghinak@superannotate.con',
    url='https://www.superannotate.com/',
    license='MIT',
    description_file="README.md",
    entry_points={
            'console_scripts': ['superannotate_schemas = superannotate_schemas.bin.app:main']
        },
      )
