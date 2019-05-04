from setuptools import setup, find_packages
import encryptor

setup(
    name='encryptor',
    version=encryptor.__version__,
    author='Mark Nagovitsin',
    author_email='nagov-mark@mail.ru',
    packages=find_packages(),
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts':
            ['encryptor = encryptor.encryptor:main']
    }
)
