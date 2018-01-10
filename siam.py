from __future__ import division, print_function

import os
import json

import numpy as np
import h5py
from keras.models import Model
from matplotlib import pyplot as plt

from src.model import generate_model, compile_model
from src.train import train_model
from src.test import test_model, cmc

os.environ["CUDA_VISIBLE_DEVICES"]="0"

def siamRD(model_parameters_path="model_parameters.json",
            b_load_weights=False,
            b_train_model=False,

    # Read infos from json
    with open(model_parameters_path, "r") as f:
        model_data = json.loads(f.read())

    # Generate model
    model = generate_model()
    model = compile_model(model)
    if verbose:
        model.summary()

    # Load weights
    if b_load_weights:
        model.load_weights(os.path.join("weights", model_data["weights_file"]))

    # Train
    if b_train_model:
        batch_size = model_data["batch_size"]
        batch_per_epoch = model_data["batch_per_epoch"]
        epochs = model_data["epochs"]
        batch_per_valid = model_data["batch_per_valid"]
        with h5py.File(model_data["dataset_path"], "r") as f:
            histo = train_model(model, f, batch_size=batch_size, steps_per_epoch=batch_per_epoch, epochs=epochs, validation_steps=batch_per_valid)

    # Test
    if b_test_model:
        cmc(model)

if __name__ == '__main__':
    siamRD()
