# Judge books by their cover using Flux.jl
Create a machine learning model to predict the category of a book from its cover image. Link containing zip file with BSON weights: https://drive.google.com/open?id=127FsMYnUA2jV8sjRw7nAx0b3cHdJ-vOQ


### 1. Pre-processing
1. Center crop to (224,224,1): To counter Out of Memory issues, I have performed center crop on dataset images to yield dimensions of (224,224,1)
2. I filter 160 images from the dataset, which are either covers which have been removed from Amazon, or greyscale images in this RGB dataset. This leaves me with 51150 train images and 5685 test images.
3. Due to memory issues, I further reduce my dataset to use 15000 training images and 510 test images. 15000 and 510 are both divisible by 30 (ensuring a balanced dataset)
4. I randomly shuffle my training set


### 2. Model & Hyperparameters
The following is my model architecture. The first 3 dense layers are followed by reLU activation functions, while the last layer is followed by the softmax output function. I use the cross entropy loss function and the Adam optimiser with a learning rate of 1e-04.
<pre>
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
flatten_1 (Flatten)          (None, 50176)              0
_________________________________________________________________
dense_1 (Dense)              (None, 4096)               356055992
_________________________________________________________________
dense_2 (Dense)              (None, 4096)               16781312
_________________________________________________________________
dense_2 (Dense)              (None, 4096)               16781312 
_________________________________________________________________
dense_3 (Dense)              (None, 30)                 122910 
=================================================================
Total params: 389,741,526
Trainable params: 389,741,526
Non-trainable params: 0
_________________________________________________________________
</pre>


### 3. Experiments
1. VGGnet and Alexnet: Both of these models consist of Conv layers, which had to be removed in order to counter the stagnant accuracy problem.
2. 4 dense layers model: This model achieved 10.98 accuracy over 20 epochs. During experimentation, I discovered that a larger batch size is ideal for model training on this dataset, afetr having experimented with sizes of 30, 150, 750, 1000,  and 5000. Apart from benchmarking the accuracy of my model, I also measure the mean epoch training time in Flux to be 4.99 seconds per epoch on 1 12GB GTX Titan X GPU.


