import torch


class MyModel(torch.nn.Module):
    def __init__(
        self, input_size: int = 64 * 64, hidden_size: int = 128, output_size: int = 15
    ):
        super().__init__()

        self.model = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, output_size),
        )

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)
        return self.model(x)
