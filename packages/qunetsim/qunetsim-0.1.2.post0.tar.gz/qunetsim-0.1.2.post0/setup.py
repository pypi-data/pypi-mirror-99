import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='qunetsim',
    version='0.1.2post0',
    scripts=['bin/template'],
    author="Stephen DiAdamo, Janis Nötzel, Benjamin Zanger, Mert Mehmet Bese",
    author_email="stephen.diadamo@gmail.com",
    description="A Quantum Network Simulation Framework",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tqsd/QuNetSim",
    download_url="https://github.com/tqsd/QuNetSim/releases/tag/0.1.2",
    keywords=['quantum', 'networks', 'simulator', 'internet', 'QuNetSim'],
    install_requires=[
        'eqsn',
        'networkx',
        'numpy',
        'scipy',
        'matplotlib',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
)
