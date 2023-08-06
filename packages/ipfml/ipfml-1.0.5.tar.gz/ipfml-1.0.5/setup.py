from setuptools import setup
import distutils.command.check

class TestCommand(distutils.command.check.check):
    """Custom check command."""

    def run(self):

        # run tests using doctest
        import doctest
        
        # filters folder
        from ipfml.filters import noise as noise_filters
        from ipfml.filters import kernels as kernels_filters
        from ipfml.filters import convolution as convolution_filters
        
        # iqa folder
        from ipfml.iqa import fr as fr_iqa

        # metrics folder
        from ipfml import metrics

        # processing folder
        from ipfml.processing import compression as compression_processing
        from ipfml.processing import movement as movement_processing
        from ipfml.processing import reconstruction as reconstruction_processing
        from ipfml.processing import segmentation as segmentation_processing
        from ipfml.processing import transform as transform_processing

        # utils 
        from ipfml import utils

        print("==============================")
        print("Runs test command...")

        # noise folder
        doctest.testmod(noise_filters)
        doctest.testmod(kernels_filters)
        doctest.testmod(convolution_filters)

        # iqa folder
        doctest.testmod(fr_iqa)

        # metrics folder
        doctest.testmod(metrics)

        # processing folder
        doctest.testmod(compression_processing)
        doctest.testmod(movement_processing)
        doctest.testmod(reconstruction_processing)
        doctest.testmod(segmentation_processing)
        doctest.testmod(transform_processing)

        # utils 
        doctest.testmod(utils)

        print('check done')
        distutils.command.check.check.run(self)


setup(
    name='ipfml',
    version='1.0.5',
    description='Image Processing For Machine Learning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    url='https://github.com/prise-3d/ipfml',
    author='Jérôme BUISINE',
    author_email='jerome.buisine@univ-littoral.fr',
    license='MIT',
    packages=['ipfml', 'ipfml/filters', 'ipfml/iqa', 'ipfml/processing'],
    install_requires=[
        'numpy',
        'Pillow',
        'sklearn',
        'scikit-image',
        'scipy',
        'opencv-python',
    ],
    cmdclass={
        'test': TestCommand,
    },
    zip_safe=False)
