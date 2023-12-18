from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
import cv2
import math
import keras

# Replicate results
keras.utils.set_random_seed(42)
np.random.seed(42)

TRAIN_DIR = 'data/images/test'
TEST_DIR = 'data/images/train'

input_shape = (32, 32, 1)
batch_size = 32
epochs = 30
conv_blocks = 3
dense_blocks = 2
model_name = 'TicTacToeClassifier'


def load_img(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # Fit to input size
    img = cv2.resize(img, (32, 32))
    img = np.expand_dims(img, axis=-1)
    return img.astype(np.float32)

# loads data from directory
def load_data(base_dir):
    X, y = [], []

    for  _, class_dirs, _ in os.walk(base_dir):
        for idx, class_dir in enumerate(class_dirs):

            image_dir = os.path.join(base_dir, class_dir)
            class_images = os.listdir(image_dir)

            # populates y with respective labels
            y.extend(np.tile(idx, len(class_images)))

            for img in class_images:
                img = load_img(os.path.join(image_dir, img))
                X.append(img)

    y = to_categorical(y)
    return np.asarray(X), np.asarray(y)

# Generates convolutional blocks to attach to CNN --> helps with understanding the image
def generate_conv_block(model, is_input=False):
    if is_input:
        model.add(Conv2D(64, (3, 3), input_shape=input_shape, padding='same'))
    else:
        model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))   
    return model

# Generates dense blocks to attach to CNN --> helps with understanding the relationship between latent feature space and given label
def generate_dense_block(model, add_dropout_layer=False):
    model.add(Dense(64))
    model.add(Activation('relu'))
    if add_dropout_layer:
        model.add(Dropout(0.4))
    return model


# reshape image to match model's input shape, used for predicting on live data
def reshape_input(img):
    print(img.shape)
    img = cv2.resize(img, (32, 32))

    # add dims for channel_last and batch size
    img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)
    return img.astype(np.float32) / 255


if __name__ == "__main__":
    X_train, y_train = load_data(TRAIN_DIR)
    X_test, y_test = load_data(TEST_DIR)

    print('{} instances for training'.format(len(X_train)))
    print('{} instances for evaluation'.format(len(X_test)))

    # Step 0. Build and compile model
    model = Sequential()

    for i in range(conv_blocks):
        if i == 0:
            model = generate_conv_block(model, is_input=True)
        model = generate_conv_block(model)

    model.add(Flatten()) # add a flatten layer so that the latent feature space can be ingested by the dense layers

    for i in range(dense_blocks):
        if i == dense_blocks - 1:
            model = generate_dense_block(model, add_dropout_layer=True)
        else:
            model = generate_dense_block(model)

    model.add(Dense(3, activation='softmax')) # this is the output layer; there are 3 labels, hence 3 nodes

    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    # 1. Create train generator that manipulates the image to help improve the training & reduce overfitting
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.15)
    train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size, subset='training')
    val_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size, subset='validation')

    # 2. Train the model
    print('Training model...')
    history = model.fit(
        train_generator,
        steps_per_epoch=math.ceil(len(X_train) / batch_size),
        validation_data=val_generator,
        epochs=epochs)

    # 3. Evaluate the model
    print('Evaluating model...')
    test_datagen = ImageDataGenerator(rescale=1 / 255)
    X_test, y_test = next(test_datagen.flow(X_test, y_test, batch_size=batch_size))
    loss, acc = model.evaluate(X_test, y_test, batch_size=batch_size)

    # 4. Save model
    print('Saving model...')
    model.save(f'model/{model_name}.h5')
