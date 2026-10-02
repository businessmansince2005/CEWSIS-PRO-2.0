import torch
import torch.nn as nn

class LSTMAutoencoder(nn.Module):
    def __init__(self, input_dim=128, hidden_dim=64, num_layers=1):
        super().__init__()
        self.encoder = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.decoder = nn.LSTM(hidden_dim, input_dim, num_layers, batch_first=True)

    def forward(self, x):
        # x: (batch, seq, feat)
        _, (h, _) = self.encoder(x)
        h = h[-1].unsqueeze(1).repeat(1, x.size(1), 1)
        out, _ = self.decoder(h)
        return out
