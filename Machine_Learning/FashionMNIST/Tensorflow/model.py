import keras as K

def add_layers(channels, kernels, net):
    for i in range(3):
        net.add(K.layers.ZeroPadding2D(padding=1))
        net.add(K.layers.Conv2D(channels[i], kernels, padding="valid", activation="relu"))
        net.add(K.layers.MaxPooling2D(2,2, padding="valid"))
    return net

def create():
	net = add_layers([16, 32, 64], 3, K.Sequential())
	net.add(K.layers.Flatten()) # check if interferes with batch dim, might need to add Reshape layer
	net.add(K.layers.Dense(72, activation="relu"))
	net.add(K.layers.Dense(10, activation="softmax")) # Do I need to add softmax for any reason??
	return net

