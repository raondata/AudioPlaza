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
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
