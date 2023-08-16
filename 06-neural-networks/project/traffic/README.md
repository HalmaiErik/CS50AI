My experimentation mostly consisted of trying different filter amounts, kernel sizes, pooling techniques, dropout rates
and number of hidden layers.
I have found that having a smaller amount of filters, with a bigger kernel size, in the first convolutional layer, gave
better results than having 32 3x3 filters, like in the example from the lecture. Not only this, but it also reduced the
number of parameters by a significant amount, from 100k+ to around 78.9k. This is why a choose 16 4x4 filters. After this
convolutional layer, I added a MaxPooling layer, which I found to give better results then the AveragePooling one.
For the second convolutional layer, I tried repeating the same convolutional layer from before, but it gave a high loss,
thus I experimented with 32 and 64 filters. I found that 64 3x3 filters gave the best result. I decided to reduce the
kernel size, because the results were similar to a 4x4 kernel size, but with a higher number of parameters. I also found
that an AveragePooling layer gave better results than a MaxPooling one.
Adding other hidden layers beside these will not increase accuracy by a significant amount, but the number of parameters
will increase exponentially, thus I decided against it.
I found that a droput layer with a 0.5 rate reduced overfitting by the most amount.