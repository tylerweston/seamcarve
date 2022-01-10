from setuptools import find_packages, setup

setup(
    name="seamcarve",
    packages=find_packages(include=['seamcarvelib']),
    version="0.0.1",
    description="Seam Carving",
    author="Tyler Weston",
    license="MIT",
    install_requires=['opencv-python', 'ffmpeg-python'],
    setup_requires=['flake8', 'pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests.test_seamcarve',
)
