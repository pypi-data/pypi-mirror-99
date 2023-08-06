import setuptools
import foxTemplateEngine


with open('readme.md') as fr:
    long_description = fr.read()


setuptools.setup(
    name='foxTemplateEngine',
    version=foxTemplateEngine.__version__,
    author='Petrov D.A.',
    author_email='leroykid02@mail.ru',
    description='Template Engine for HTML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/leroykiddd/templateEngine',
    packages=setuptools.find_packages(),
    install_requires=[
        
    ],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)
