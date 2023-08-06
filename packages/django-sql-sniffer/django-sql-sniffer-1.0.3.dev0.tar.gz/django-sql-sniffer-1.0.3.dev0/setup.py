import setuptools
import django_sql_sniffer


URL = 'https://github.com/gruuya/django-sql-sniffer'
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = long_description.replace('![demo](demo.webp)', f'[demo]({URL})\\')


setuptools.setup(
    name='django-sql-sniffer',
    version=django_sql_sniffer.version,
    description='Django SQL Sniffer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='django sql query remote process analysis',
    url=URL,
    author='Marko Grujic',
    author_email='markoog@gmail.com',
    license='MIT',
    install_requires=['django'],
    python_requires='>=3.5',
    packages=['django_sql_sniffer'],
    entry_points=dict(
        console_scripts=[
            'django-sql-sniffer = django_sql_sniffer.listener:main'
        ]
    )
)
