from setuptools import setup

setup(
    name='XnatUploadToolDicom',
    version='1.4.0.2',
    description='Tool for assisting in uploading dicom data directly to xnat imaging research platform (xnat.org)',
    packages=['XnatUploadToolDicom'],
    scripts=['scripts/xnat-uploader-dicom'],
    author='Brian Holt',
    author_email='brian@radiologics.com',
    license='BSD 3-Clause License',
    keywords='xnat',
    python_requires='>=2.6',
    classifiers=[
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2',
    ],
    url='https://bitbucket.org/radiologics/XnatUploadToolDicom',
    install_requires=[
        "requests>=2.18.4",
        "EasyProcess>=0.2.3",
        "pyunpack>=0.1.2",
        "mime>=0.1.0",
        "pydicom >= 1.0.0",
        "patool>=1.12",
        "python-magic>=0.4.14",
        "pathos>=0.2.1",
        "ConfigArgParse>=0.13.0",
        "ConfigParser",
        "natsort>=5.5.0",
        "jsbeautifier>=1.13.0",
        "dirhash>=0.2.1"
    ]
)
