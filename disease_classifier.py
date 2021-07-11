import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import BatchNormalization, Lambda, Input, Dense, Convolution2D, MaxPooling2D, Dropout, \
    Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD
from keras.layers.merge import Concatenate


train_path = 'E:/Projects/PES sem 3/NewData/Train'
test_path = 'E:/Projects/PES sem 3/data/Train'


class MyCall(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if logs is None:
            logs = {}
        if logs.get('accuracy') > 0.98:
            self.model.stop_training = True


train_datagen = ImageDataGenerator(rescale=1./255,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   rotation_range=40,
                                   zoom_range=0.2,
                                   shear_range=0.2,
                                   horizontal_flip=True,
                                   vertical_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(train_path,
                                               target_size=(224, 224),
                                               class_mode='categorical',
                                               batch_size=32,
                                               shuffle=True)

test_data = test_datagen.flow_from_directory(test_path,
                                             target_size=(224, 224),
                                             class_mode='categorical')


def my_model():
    input_image = Input(shape=(224, 224, 3))
    top_conv1 = Convolution2D(filters=48, kernel_size=(11, 11), strides=(4, 4),
                              input_shape=(224, 224, 3), activation='relu')(input_image)
    top_conv1 = BatchNormalization()(top_conv1)
    top_conv1 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(top_conv1)

    top_top_conv2 = Lambda(lambda x: x[:, :, :, :24])(top_conv1)
    top_bot_conv2 = Lambda(lambda x: x[:, :, :, 24:])(top_conv1)

    top_top_conv2 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        top_top_conv2)
    top_top_conv2 = BatchNormalization()(top_top_conv2)
    top_top_conv2 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(top_top_conv2)

    top_bot_conv2 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        top_bot_conv2)
    top_bot_conv2 = BatchNormalization()(top_bot_conv2)
    top_bot_conv2 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(top_bot_conv2)

    top_conv3 = Concatenate()([top_top_conv2, top_bot_conv2])
    top_conv3 = Convolution2D(filters=192, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        top_conv3)

    top_top_conv4 = Lambda(lambda x: x[:, :, :, :96])(top_conv3)
    top_bot_conv4 = Lambda(lambda x: x[:, :, :, 96:])(top_conv3)

    top_top_conv4 = Convolution2D(filters=96, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        top_top_conv4)
    top_bot_conv4 = Convolution2D(filters=96, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        top_bot_conv4)

    top_top_conv5 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        top_top_conv4)
    top_top_conv5 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(top_top_conv5)

    top_bot_conv5 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        top_bot_conv4)
    top_bot_conv5 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(top_bot_conv5)

    bottom_conv1 = Convolution2D(filters=48, kernel_size=(11, 11), strides=(4, 4),
                                 input_shape=(224, 224, 3), activation='relu')(input_image)
    bottom_conv1 = BatchNormalization()(bottom_conv1)
    bottom_conv1 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(bottom_conv1)

    bottom_top_conv2 = Lambda(lambda x: x[:, :, :, :24])(bottom_conv1)
    bottom_bot_conv2 = Lambda(lambda x: x[:, :, :, 24:])(bottom_conv1)

    bottom_top_conv2 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        bottom_top_conv2)
    bottom_top_conv2 = BatchNormalization()(bottom_top_conv2)
    bottom_top_conv2 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(bottom_top_conv2)

    bottom_bot_conv2 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        bottom_bot_conv2)
    bottom_bot_conv2 = BatchNormalization()(bottom_bot_conv2)
    bottom_bot_conv2 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(bottom_bot_conv2)

    bottom_conv3 = Concatenate()([bottom_top_conv2, bottom_bot_conv2])
    bottom_conv3 = Convolution2D(filters=192, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        bottom_conv3)

    bottom_top_conv4 = Lambda(lambda x: x[:, :, :, :96])(bottom_conv3)
    bottom_bot_conv4 = Lambda(lambda x: x[:, :, :, 96:])(bottom_conv3)

    bottom_top_conv4 = Convolution2D(filters=96, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        bottom_top_conv4)
    bottom_bot_conv4 = Convolution2D(filters=96, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        bottom_bot_conv4)

    bottom_top_conv5 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        bottom_top_conv4)
    bottom_top_conv5 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(bottom_top_conv5)

    bottom_bot_conv5 = Convolution2D(filters=64, kernel_size=(3, 3), strides=(1, 1), activation='relu', padding='same')(
        bottom_bot_conv4)
    bottom_bot_conv5 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(bottom_bot_conv5)

    conv_output = Concatenate()([top_top_conv5, top_bot_conv5, bottom_top_conv5, bottom_bot_conv5])

    flatten = Flatten()(conv_output)

    FC_1 = Dense(units=4096, activation='relu')(flatten)
    FC_1 = Dropout(0.6)(FC_1)
    FC_2 = Dense(units=4096, activation='relu')(FC_1)
    FC_2 = Dropout(0.6)(FC_2)
    output = Dense(units=2, activation='softmax')(FC_2)

    model = Model(inputs=input_image, outputs=output)

    sgd = SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)

    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


model = my_model()
model.summary()

model.fit_generator(train_data,
                    validation_data=test_data,
                    epochs=10,
                    callbacks=MyCall())

model.save('final_classifier.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.post_training_quantize = True
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
tflite_model_name = "final_classifier.tflite"
open(tflite_model_name, "wb").write(tflite_model)

