from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

from augmentor import p

img_size = 32
model = Sequential()
model.add(Conv2D(48, (3, 3), strides=1, padding='same', \
                activation='relu', input_shape=(img_size, img_size, 3)))
model.add(Conv2D(64, (3, 3), strides=1, padding='same', \
                activation='relu', input_shape=(img_size, img_size, 3)))
model.add(Conv2D(128, (3, 3), strides=1, padding='same', \
                activation='relu', input_shape=(img_size, img_size, 3)))
model.add(MaxPooling2D())
model.add(Dropout(0.22))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(15, activation='softmax'))
opt = Adam()
model.compile(loss='categorical_crossentropy', optimizer=opt, \
        metrics=['accuracy'])

g = p.keras_generator(batch_size=128)

model.fit_generator(g, steps_per_epoch=500, epochs=30, \
        validation_data=g, validation_steps=500)
model.save('model.h5')
