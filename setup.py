from setuptools import setup

setup(
    name='gb_api_tools',
    version='0.0.1',
    python_requires='>=3.6',
    author_email='michael.way@generalbioinformatics.com',
    license_files = ('LICENSE.txt'),
    install_requires=[
        'pandas==1.1.5',
        'requests==2.26.0',
        'openpyxl==3.0.0',
        'biopython==1.74'
        ],
    include_package_data=True
    )
