# Install keras

We can install the `Keras` package from PyPI using this command:

    >>> quiet("guild install 'keras<2.4'")

And the installed version:

    >>> run("guild packages list -a keras")
    Keras                2.3...  Deep Learning for humans
    Keras-Applications   1.0...  Reference implementations of popular deep learning models
    Keras-Preprocessing  1.1...  Easy data preprocessing and data augmentation ...
    <exit 0>

We need to make sure h5py is installed for Keras checkpoints to be
created.

    >>> quiet("pip install 'h5py<3' --upgrade --force")
