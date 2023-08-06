from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

with open(here / "requirements.txt", "r") as f:
    requirements = f.read().split("\n")


setup(
    name='anysell',
    version='0.0.3',
    description='Sell any item you want on any market platform easily.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/maroshmka/anysell',
    author='Mário Hunka',
    author_email='hunka.mario@gmail.com',
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='automatization, sale, goods, cli',
    package_dir={'': 'anysell'},
    packages=find_packages(where='anysell'),
    python_requires='>=3.6, <4',

    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'anysell=anysell.main:cli',
        ],
    },
)
