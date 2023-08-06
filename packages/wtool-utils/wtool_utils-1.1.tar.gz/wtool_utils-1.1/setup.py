from setuptools import setup, find_packages
from setuptools.command.install import install


class InstallSetupScript(install):
    def run(self):
        try:
            self.spawn(['sudo', 'apt-get', 'update'])
            self.spawn(['sudo', 'apt-get', 'install', '-y',
                        'python3-dev', 'python3-pip',
                        'libpcap-dev', 'cython3'])
        except Exception as e:
            print(e)
        super().run()


setup(
    long_description=open("README.md", "r").read(),
    name="wtool_utils",
    version="1.1",
    description="helper for the wtool app",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/wtool_utils",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': [
            'wtool_utils = wtool_utils.__main__:main'
        ]
    },
    cmdclass={
        'install': InstallSetupScript
    },
    keywords="companion script wtool utils",
    packages=find_packages(),
    install_requires=["netifaces", "python-libpcap", "bson"],
    long_description_content_type="text/markdown",
)
