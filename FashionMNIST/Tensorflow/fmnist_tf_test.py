import os
import keras as K
#import model

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" # mute annoying warning
#file_num = input("Which file number to test? ")
#model_name = "models/fmnist_tf" + file_num + ".h5"
model_name = "models/fmnist_tf1.h5"

FMNIST = K.datasets.fashion_mnist
(x_train, y_train), (x_test, y_test) = FMNIST.load_data()
x_test, y_test = x_test.reshape(x_test.shape[0], 28, 28, 1), K.utils.to_categorical(y_test)

#ConvNet = model.create()

#ConvNet.compile(
#    loss="categorical_crossentropy",
#    optimizer=K.optimizers.Adam(lr=1e-04),
#    metrics=["acc"])

ConvNet = K.models.load_model(model_name)

scores = ConvNet.evaluate(x_test, y_test, verbose=1)
print('Test accuracy:', scores[1])

