using Flux, Statistics
using Flux: onehotbatch, onecold, crossentropy, throttle
using Base.Iterators: repeated, partition
using CSV, FileIO
using Images
using Printf, BSON
using BSON: @load

train_path, test_path = "/home/summervisitor2/julia/bin/data/train/", "/home/summervisitor2/julia/bin/data/test/"

train_ = CSV.read(train_path * "train3.csv", header=["fname", "class", "rand"])
test_ = CSV.read(test_path * "test3.csv", header=["fname", "class"])

# To array for easier computation
train_imgs, test_imgs = collect(train_.fname), collect(test_.fname)
train_lbs, test_lbs = collect(train_.class), collect(test_.class)

train_size, test_size = length(train_lbs), length(test_lbs)

function mb(path, img, label, indices)
    temp = length(indices)
    mb_x = Array{Float32}(undef, (224, 224, 1)..., temp) #pre-allocation to speed up process
    for i in 1:temp
        path_ = path * img[i]
        mb_x[:, :, :, i] = Float32.(reshape(channelview(load(path_)), (224,224,1))) #reshape to channels last representation
    end
    # This encodes labels into one-hot vector representation
    mb_y = onehotbatch(label[indices], 0:29)
    return (mb_x, mb_y)
end


mb_size = 5000 
mb_idxs = partition(1:train_size, mb_size)

# Define datasets
trainset = [mb(train_path, train_imgs, train_lbs, i) for i in mb_idxs] |> gpu
testset = mb(test_path, test_imgs, test_lbs, 1:test_size) |> gpu

Alexnet1 = Chain(
    x -> reshape(x, :, size(x, 4)),
    Dense(50176, 4096, relu), ##wait for dims mismatch to change
    Dense(4096, 4096, relu),
    Dense(4096, 4096, relu),
    Dense(4096, 30),
    softmax
) |> gpu


loss(x, y) = crossentropy(Alexnet1(x), y)

accuracy(x, y) = mean(Flux.onecold(Alexnet1(x)) .== Flux.onecold(y))

optimiser = ADAM(0.0001) #AMSGrad() >> default:(0.001, (0.9, 0.999))
best_acc, last_improvement, epoch_num, threshold = 0.0, 0, 500, 0.95 #need more epochs due to small batch size (sorta like SGD)
time = 0
for i in 1:epoch_num
    tic = time_ns()
    Flux.train!(loss, params(Alexnet1), trainset, optimiser)
    toc = time_ns()
    global time += toc-tic
    println(time)
    acc = accuracy(testset...)
    if acc > best_acc
        md2 = cpu(Alexnet1)
        BSON.@save joinpath("books_Alexnet2.bson") md2
        global best_acc = acc
        println("New best accuracy!")
    end
    println("Epoch ", i, ": ", acc)
    println(Flux.onecold(Alexnet1(testset[1][:,:,:, 1:5])))
    println("\n")
end
