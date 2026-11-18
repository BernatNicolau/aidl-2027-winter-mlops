from pathlib import Path

import torch
from dataset import MyDataset
from model import MyModel

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")


def train_single_epoch():
    # TODO: Implement training loop
    raise NotImplementedError


def eval_single_epoch():
    # TODO: Implement evaluation loop
    raise NotImplementedError


def train_model(config):

    my_dataset = MyDataset(
        images_path=config["images_path"], labels_path=config["labels_path"]
    )
    my_model = MyModel(hidden_size=config["hidden_size"]).to(device)

    for epoch in range(config["epochs"]):
        train_single_epoch(...)
        eval_single_epoch(...)

    return my_model


if __name__ == "__main__":
    DATA_DIR = Path(__file__).parent / "data"
    config = {
        "images_path": DATA_DIR / "data" / "data",
        "labels_path": DATA_DIR / "chinese_mnist.csv",
        "epochs": 5,
        "hidden_size": 128,
        "lr": 0.01,
        "batch_size": 100,
    }

    train_model(config)
