import setuptools

setuptools.setup(
    name='common_structure_microservices',
    packages=['common_structure_microservices'],
    version='0.0.16',
    description='Este es un paquete que permite utilizar cosas comunes a los microservicios con solo instalarlo '
                'mediante pip',
    author='Paola Pájaro & Fernando Romero <3',
    author_email='juanfernandoro@ufps.edu.co, yindypaolapu@ufps.edu.co',
    url='https://github.com/fernanxd17, https://github.com/PaolaBird',  # use the URL to the github repo
    download_url='https://PaolaBird@bitbucket.org/PaolaBird/common_microservices.git',
    install_requires=["Django", 'djangorestframework', 'djongo', 'requests',
                      'django-filter', 'setuptools', 'drf-yasg', 'munch', 'threaded-task-executor',
                      'python-dateutil'],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
