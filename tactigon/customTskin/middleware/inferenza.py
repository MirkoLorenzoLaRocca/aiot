import torch
import torch.nn as nn
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes, dropout):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
        self.batch_norm = nn.BatchNorm1d(hidden_size)  # Apply normalization across the hidden layer dimension
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # LSTM returns output and hidden states; we only use the output
        out, _ = self.lstm(x)
        # Apply batch normalization to the output of the last time step
        out = self.batch_norm(out[:, -1, :])
        # Fully connected layer for classification
        out = self.fc(out)
        return out
    
# Model parameters
input_size = 8  
hidden_size = 512
num_layers = 3
num_classes = 4
dropout = 0.2

# Initialize the model
device = "cpu"  # Use MPS if available
model = LSTMModel(input_size, hidden_size, num_layers, num_classes, dropout).to(device)

# Load the trained model weights
model.load_state_dict(torch.load("best_model2.pth", map_location=device))
model.eval()  # Set the model to evaluation mode