from setuptools import setup

setup(name='SuperAnnotateSchemas',
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
