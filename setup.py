from setuptools import setup, find_packages

setup(
    name='jupyter_export_html_style',
    version='0.1.0',
    description='A JupyterLab extension that exports notebooks as HTML with cell style metadata overrides',
    author='gb119',
    packages=find_packages(),
    install_requires=[
        'nbconvert>=6.0.0',
        'jupyter>=1.0.0',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        'jupyter_export_html_style': ['templates/*.j2'],
    },
    entry_points={
        'nbconvert.exporters': [
            'html_style = jupyter_export_html_style.exporter:HTMLStyleExporter',
        ],
    },
)
