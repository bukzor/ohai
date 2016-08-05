"""A demo of reliable pth installation, with a dash of troll."""
from distutils import log

from setuptools import setup
from setuptools.command.install import install as orig_install

PTH = '''\
from sys import stderr
stderr.write(%r)
'''

DOC = __doc__


class Install(orig_install):
    """
    default semantics for install.extra_path cause all installed modules to go
    into a directory whose name is equal to the contents of the .pth file.

    All that was necessary was to remove that one behavior to get what you'd
    generally want.
    """
    def initialize_options(self):
        orig_install.initialize_options(self)
        name = self.distribution.metadata.name

        contents = PTH % open('ohai.dat').read()
        contents = 'import sys; exec(%r)\n' % contents
        self.extra_path = (name, contents)

    def finalize_options(self):
        orig_install.finalize_options(self)

        from os.path import relpath, join
        install_suffix = relpath(self.install_lib, self.install_libbase)
        if install_suffix == '.':
            log.info('skipping install of .pth during easy-install')
        elif install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase
            log.info(
                "will install .pth to '%s.pth'",
                join(self.install_lib, self.extra_path[0]),
            )
        else:
            raise AssertionError(
                'unexpeceted install_suffix',
                self.install_lib, self.install_libbase, install_suffix,
            )


def main():
    """the entry point"""
    from textwrap import dedent

    setup(
        name='ohai',
        version='1!0',
        url="https://github.com/bukzor/ohai",
        license="MIT",
        author="Buck Evan",
        author_email="buck.2019@gmail.com",
        description=DOC,
        long_description=dedent(Install.__doc__),
        zip_safe=False,
        classifiers=[
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'License :: OSI Approved :: MIT License',
        ],
        cmdclass={
            'install': Install,
        },
        options={
            'bdist_wheel': {
                'universal': 1,
            },
        },
    )


if __name__ == '__main__':
    exit(main())
