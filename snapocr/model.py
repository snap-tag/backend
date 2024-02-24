from torch import nn

class CNNModel(nn.Module):
    def __init__(self, num_classes):
        super(CNNModel, self).__init__()

        # parameters for Convolutional Layers
        filter_dim = 3
        in_channels = [1, 64, 56]
        out_channels = [64, 56, 40]
        pool_dim = 2

        # initializing all the layers
        self.c1 = nn.Conv2d(in_channels=in_channels[0], out_channels=out_channels[0], kernel_size=filter_dim, padding="same")
        self.c2 = nn.Conv2d(in_channels=in_channels[1], out_channels=out_channels[1], kernel_size=filter_dim, padding="same")
        self.c3 = nn.Conv2d(in_channels=in_channels[2], out_channels=out_channels[2], kernel_size=filter_dim, padding="same")

        self.batch_norm1 = nn.BatchNorm2d(out_channels[0])
        self.batch_norm2 = nn.BatchNorm2d(out_channels[1])
        self.batch_norm3 = nn.BatchNorm2d(out_channels[2])

        self.dropout = nn.Dropout(0.5)

        self.relu = nn.ReLU()

        self.max_pool = nn.MaxPool2d(kernel_size=pool_dim)

        self.fc = nn.Linear(out_channels[2] * 3 * 3, num_classes)

        self.softmax = nn.Softmax(dim=1)


    def forward(self, X):
        x = self.c1(X)
        x = self.batch_norm1(x)
        x = self.relu(x)
        x = self.max_pool(x)

        x = self.c2(x)
        x = self.batch_norm2(x)
        x = self.relu(x)
        x = self.max_pool(x)

        x = self.c3(x)
        x = self.batch_norm3(x)
        x = self.relu(x)
        x = self.max_pool(x)

        x = x.view(x.size(0), -1)

        x = self.fc(x)
        x = self.softmax(x)

        return x
