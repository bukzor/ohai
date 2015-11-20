"""A demo of reliable pth installation, with a dash of troll."""
from distutils import log

from setuptools import setup
from setuptools.command.install import install as orig_install

PTH = '''\
from sys import stderr
stderr.write(%r)
'''


class Install(orig_install):
    """default semantics for install.extra_path cause all installed modules to
    go into a directory whose name is equal to the contents of the .pth file.
    
    I undo just that specific behavior here.
    """
    def initialize_options(self):
        orig_install.initialize_options(self)
        name = self.distribution.metadata.name

        contents = PTH % open('ohhi.dat').read()
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
    setup(
        name='ohhi',
        version='3!0',
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
