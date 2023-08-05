from distutils.core import setup

setup(
    name='pltanimation',
    packages=['pltanimation'],
    version='0.2',
    license='MIT',
    description='Build matplotlib animation with animation-block sequences',
    author='Liubomyr Ivanitskyi',
    author_email='lubomyr.ivanitskiy@gmail.com',
    url='https://github.com/LubomyrIvanitskiy',
    download_url='https://github.com/LubomyrIvanitskiy/PLTAnimation/archive/0.2.tar.gz',
    keywords=['matplotlib', 'animation', 'plot', "builder", "sequence"],
    install_requires=[
        'abc',
        'matplotlib',
        'webbrowser',
        'typing',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
