import setuptools

from AudioPlaza import __version__

setuptools.setup(
    name="AudioPlaza",
    version=__version__,
    license='Raondata Private',
    author="RAONDATA speech team",
    author_email="kojunseo@raondata.ai",
    description="AudioPlaza: RAONDATA speech team's Audio Preprocessing written by python",
    long_description=open('README.md').read(),
    url="https://www.raondata.ai",
    packages=setuptools.find_packages(),
    package_data={'AudioPlaza': [
        'src/*',
    ]},
    python_requires='>=3.6',
)
