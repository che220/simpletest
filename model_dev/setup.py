from setuptools import setup, find_packages

setup(
    # Package information
    name='model_dev',
    version='1.0.0',

    # Package data
    # packages=find_packages(),
    packages=['model', 'training', 'inference'],
    include_package_data=True,
    url='https://www.github.com/che220/model_dev',

    # Insert dependencies list here
    install_requires=[
        'pandas',
        'scipy',
        'scikit-learn',
        'tensorflow'
    ],
    entry_points={
        'setuptools_docker.train': [
            'my_training_entrypoint = training.train:train',
        ],
        'setuptools_docker.predict': [
            'my_prediction_entrypoint = inference.predict:predict',
        ]
    }
)
