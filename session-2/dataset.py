from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import DataLoader, random_split
from torchvision.io import read_image


class MyDataset(torch.utils.data.Dataset):
    def __init__(self, images_path: Path, labels_path: str | Path):
        super().__init__()
        self.images_path = Path(images_path)
        self.labels_path = Path(labels_path)
        self.labels = pd.read_csv(self.labels_path)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        thislabel = self.labels.iloc[idx]
        image_path = (
            self.images_path
            / f"input_{thislabel['suite_id']}_{thislabel['sample_id']}_{thislabel['code']}.jpg"
        )
        image = read_image(str(image_path)).float() / 255.0
        label = thislabel["code"] - 1
        label_tensor = torch.tensor(label, dtype=torch.long)
        return image, label_tensor


def get_dataloaders(
    images_path: Path, labels_path: str | Path, batch_size: int = 64, seed=0
):
    dataset = MyDataset(images_path, labels_path)
    dataset_train, dataset_validate, dataset_test = random_split(dataset)
    data_loader = DataLoader(dataset, batch_size, True)
