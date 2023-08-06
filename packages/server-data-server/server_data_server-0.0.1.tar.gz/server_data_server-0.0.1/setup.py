import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='server_data_server',
    version='0.0.1',
    author='Ilya Vouk',
    author_email='ilya.vouk@gmail.com',
    description='Server information server generation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/VoIlAlex/server-data-server',
    packages=setuptools.find_packages(),
    package_data={
        'server_data_server': [
            'template/**',
            'bin/*.dll',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=required,
    entry_points={
        'console_scripts': [
            'sis=server_data_server.__main__:cli',
        ],
    },
)
