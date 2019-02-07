from setuptools import setup, find_packages
from setuptools import Extension
import numpy as np

ext_modules = [Extension('cbgt', ['src/cbgt.c'])]
package_data = {'cbgt': ['src/*.c', 'src/*.h', 'docs/*.md',
                'docs/*.txt', 'params/*.py', 'params/*.tex']}
cbgt_packages = ['cbgt', 'cbgt.analyzefx', 'cbgt.netgen', 'cbgt.sim', 'cbgt.vis']

setup(
    name='CBGT',
    version='0.0.1',
    author='Kyle Dunovan, Catalina Vich, Matthew Clapp, Timothy Verstynen, Jonathan Rubin, Wei Wei, and Xiao Jing Wang',
    author_email='dunovank@gmail.com',
    url='http://github.com/CoAxLab/bgNetwork',
    packages=cbgt_packages,
    package_data=package_data,
    description='CBGT contains code for implementing the CBGT network and drift-diffusion model (DDM) fits described in the manuscript Reward-driven changes in striatal pathway competition shape evidence evaluation in decision-making.',
    install_requires=['numpy==1.11.3', 'pandas>=0.15.1', 'matplotlib>=1.4.3', 'seaborn>=0.5.1', 'future'],
    setup_requires=['numpy==1.11.3', 'pandas>=0.15.1', 'matplotlib>=1.4.3', 'seaborn>=0.5.1', 'future'],
    include_dirs = [np.get_include()],
    classifiers=['Environment :: Console',
                'License :: OSI Approved :: BSD License',
                'Intended Audience :: Science/Research',
                'Development Status :: 3 - Alpha',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Topic :: Scientific/Engineering',
                 ],
    ext_modules = ext_modules
)
