from setuptools import setup, find_packages

setup(
    name='extract_clerk',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pytesseract',
        'pdf2image',
        'pillow',
        'PyPDF2',
    ],
    entry_points={
        'console_scripts': [
            'extract_clerk=src.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
