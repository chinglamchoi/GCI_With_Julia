"""
If GPU is available, this program will default to using GPU:0
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import tensorflow as tf
import keras as K
import model
import time
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" # mute annoying warnings

# the epoch_num is changed due to fast convergence
batch_size, epochs, lr = 64, 200, 0.001
# class_num, classes = 10, ("T-Shirt", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle Boot")

#file_num = input("Which file to save model into? ")
#model_num = "models/fmnist_tf" + file_num + ".h5"
model_name = "models/fmnist_tf.h5"

FMNIST = K.datasets.fashion_mnist
(x_train, y_train), (x_test, y_test) = FMNIST.load_data()
y_train, y_test = K.utils.to_categorical(y_train), K.utils.to_categorical(y_test)
x_train, x_test = x_train/255.0, x_test/255.0 # normalise & to float

"""
# sanity check
x_train.shape == (60000, 28, 28)
x_test.shape == (10000, 28, 28)
"""
# reshape for processing: channel last, default tf format
x_train, x_test = x_train.reshape(x_train.shape[0], 28, 28, 1), x_test.reshape(x_test.shape[0], 28, 28, 1)


"""
This is for stopping when/if the accuracy plateaus.
Not needed as the model performs very well and hits threshold.

reduce_lr = K.callbacks.callbacks.ReduceLROnPlateau(
    monitor="accuracy", 
    factor=0.1, 
    patience=25,
    min_lr=1e-06)
"""

# Early stopping for when model stops improving on best accuracy.
# Due to its quality performance, I use a lower patience in tensorflow
# than in pytorch or Flux.

ConvNet = model.create()

ConvNet.compile(
	loss="categorical_crossentropy",
	optimizer=K.optimizers.Adam(lr=lr),
	metrics=["acc"])

callback = K.callbacks.EarlyStopping(monitor='acc', patience=20)

start = time.time()
ConvNet.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    shuffle=False,
	callbacks=[callback])
end = time.time()
#ConvNet.summary()

ConvNet.save(model_name)
print('Saved trained model at %s ' % model_name)

# Score trained model.
scores = ConvNet.evaluate(x_test, y_test, verbose=1)
#print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
print(end-start)
print("\nn")
