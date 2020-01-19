# Comparison Flux, Pytorch and Tensorflow 2.0
`*`NOTE: Due to CUDA, Windows & Julia Cudnn library compatibility issues, the Flux model is trained on a CPU without GPU acceleration.

| Platform | Acc (Mean) | Acc (Std) | Train Time (s) | Trials |
| ------ | ------ | ------ | ------ | ------ |
| Flux | 0.840| 0.0438`*` | 04:42:59`*`| 5`*`
| Pytorch | 0.889 | 0.0355 | 00:15:51 | 10
| Tensorflow | 0.825 | 0.0250 | 00:16:55 | 10

Flux, Pytorch, Tensorflow are benchmarked on the FashionMNIST dataset, using the same deep Convolutional Neural Network. GPU training (Pytorch & Tensorflow) are done on 1 RTX 2070 Max-Q GPU, while CPU training is performed on an i7-9750H CPU. Criteria for gauging performance includes 1. mean accuracy and 2. standard deviation of accuracy of trained models, 3. total model training time (s). These data are obtained over 10 separte trials. Here is the ConvNet model summary:

<pre>
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
zero_padding2d_1 (ZeroPaddin (None, 30, 30, 1)         0
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 28, 28, 16)        160
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 14, 14, 16)        0
_________________________________________________________________
zero_padding2d_2 (ZeroPaddin (None, 16, 16, 16)        0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 14, 14, 32)        4640
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 7, 7, 32)          0
_________________________________________________________________
zero_padding2d_3 (ZeroPaddin (None, 9, 9, 32)          0
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 7, 7, 64)          18496
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 3, 3, 64)          0
_________________________________________________________________
flatten_1 (Flatten)          (None, 576)               0
_________________________________________________________________
dense_1 (Dense)              (None, 72)                41544
_________________________________________________________________
dense_2 (Dense)              (None, 10)                730
=================================================================
Total params: 65,570
Trainable params: 65,570
Non-trainable params: 0
_________________________________________________________________
</pre>
In terms of hyperparameters, the model depth is 3, with an epoch number of 200. Flux and Tensorflow utilise the Adam optimiser with an initial learning rate of 1e-04; Pytorch uses the Stochastic Gradient Descent optimiser with an initial learning rate of 0.1, momentum of 0.9, decay rate of 1e-06. While monitoring the training loss of my model (which reached levels of 99%, but did not translate to a comparable testing accuracy), I noticed an overfitting problem. Hence, I hypothesise that introducing batch norm or dropout layers, as well as monitoring the validation set accuracy (after splitting the trainset into trainset and validset) would be helpful in further increasing the model accuracy.
