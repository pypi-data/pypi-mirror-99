import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call


class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        f = open("version.txt", "a")
        f.write("Adding version 2.0.0")
        f.close()
        install.run(self)
    setuptools.setup(
        name='abacba',
        version='2.0.0',
        author='..',
        author_email='',
        description='Testing OS Dependency vuln',
        packages=setuptools.find_packages(),
        install_requires=['bbbok>=0.3.0'],
        dependency_links=[],
        classifiers=(
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
        ),
    )

