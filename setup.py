from setuptools import setup
from setuptools import find_packages

setup(
    name='superannotate_schemas',
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={"": "src"},
    description='SuperAnnotate JSON Schemas',
    author='Vaghinak Basentsyan',
    author_email='vaghinak@superannotate.con',
    url='https://www.superannotate.com/',
    license='MIT',
    description_file="README.md",
    entry_points={
        'console_scripts': ['superannotate_schemas = superannotate_schemas.bin.app:main']
    },
    python_requires='>=3.6'
)
