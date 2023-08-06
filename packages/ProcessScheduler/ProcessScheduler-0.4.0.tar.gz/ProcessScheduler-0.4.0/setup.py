from setuptools import find_packages, setup

DESCRIPTION = (
      'A package to solve resource-constrained scheduling problems using SMT theory/solver.'
)

CLASSIFIERS = [
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'Intended Audience :: Manufacturing',
      'Intended Audience :: Financial and Insurance Industry',
      'Intended Audience :: Healthcare Industry',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3',
      'Topic :: Office/Business :: Scheduling',
      'Topic :: Software Development :: Libraries',
      'Typing :: Typed'
]

setup(name='ProcessScheduler',
      version='0.4.0',
      description=DESCRIPTION,
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      url='https://github.com/tpaviot/ProcessScheduler',
      author='Thomas Paviot',
      author_email='tpaviot@gmail.com',
      license='GPLv3',
      platforms="Platform Independent",
      python_requires=">=3.6",
      packages=find_packages(),
      install_requires=['z3-solver==4.8.10.0'],
      classifiers=CLASSIFIERS,
      zip_safe=True)
