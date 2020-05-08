from setuptools import setup

setup(
      name="cdetools",
      version="0.0.2",
      license="MIT",
      description="Tools for evaluating conditional density estimates.",
      author="Niccolo Dalmasso, Taylor Pospisil",
      author_email="niccolo.dalmasso@gmail.com",
      maintainer="niccolo.dalmasso@gmail.com",
      url="https://github.com/tpospisi/cdetools/python",
      classifiers=[
                   "License :: OSI Approved :: MIT License",
                   "Topic :: Scientific/Engineering :: Artificial Intelligence",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.7"
                   ],
      keywords=["conditional density estimation", "diagnostics"],
      package_dir={"": "src"},
      packages=["cdetools"],
      python_requires=">=2.7",
      install_requires=["numpy", "scipy"],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      zip_safe=False,
      include_package_data=True
      )
