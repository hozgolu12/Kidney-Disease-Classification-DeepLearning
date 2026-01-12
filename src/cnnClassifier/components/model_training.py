import os
import urllib.request as request
from zipfile import ZipFile
from cnnClassifier.entity.config_entity import TrainingConfig
import tensorflow as tf
import time
tf.config.run_functions_eagerly(True)  # For debugging purposes
from pathlib import Path


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def get_base_model(self):
        # Load model without compiling to avoid restoring optimizer state
        self.model = tf.keras.models.load_model(
            self.config.updated_base_model_path,
            compile=False
        )

        # Re-compile model appropriately depending on final output shape
        output_shape = self.model.output_shape
        # If final dim == 1 -> binary; else multi-class
        if len(output_shape) >= 2 and output_shape[-1] == 1:
            loss = "binary_crossentropy"
            optimizer = tf.keras.optimizers.Adam()
        else:
            loss = "sparse_categorical_crossentropy"
            optimizer = tf.keras.optimizers.Adam()

        self.model.compile(optimizer=optimizer, loss=loss, metrics=["accuracy"])

    def train_valid_generator(self):
        
        datagenerator_kwargs = dict(
            rescale=1.0 / 255,
            validation_split=0.20,
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        validation_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        # produce integer labels compatible with sparse_categorical_crossentropy
        self.validation_generator = validation_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            class_mode="sparse",
            **dataflow_kwargs,
        )

        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=20,
                horizontal_flip=True,
                vertical_flip=True,
                width_shift_range=0.1,
                height_shift_range=0.1,
                shear_range=0.1,
                zoom_range=0.2,
                **datagenerator_kwargs,
            )
        else:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                **datagenerator_kwargs
            )

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            class_mode="sparse",
            **dataflow_kwargs,
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    def train(self):
        self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.validation_generator.samples // self.validation_generator.batch_size

        self.model.fit(
            self.train_generator,
            steps_per_epoch=self.steps_per_epoch,
            validation_data=self.validation_generator,
            validation_steps=self.validation_steps,
            epochs=self.config.params_epochs
        )

        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )