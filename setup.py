from setuptools import setup

setup(name="envkey",
      version="1.0.0",
      description="EnvKey's python library. Protect API keys and credentials. Keep configuration in sync.",
      url="https://github.com/envkey/envkey-python",
      keywords=["security", "secrets management", "configuration management", "environment variables", "configuration", "python"],
      author="EnvKey",
      author_email="support@nvkey.com",
      license="MIT",
      packages=["envkey"],
      package_data={"envkey": ["ext/**/*"]},
      install_requires=["python-dotenv>=0.7.1"],
      download_url = 'https://github.com/envkey/envkey-python/archive/1.0.0.tar.gz',
      zip_safe=False)