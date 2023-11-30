import torch
from tqdm import tqdm

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_model(n_inputs, n_layers, n_neurons, n_outputs=20):
    """
    Create a neural network model

    Args:
        n_inputs (int): Number of input features
        n_layers (int): Number of hidden layers
        n_neurons (int): Number of neurons in each hidden layer
        n_outputs (int): Number of output features, defaults to 20

    Returns:
        torch.nn.Sequential: The model
    """

    # Create a list of layers
    layers = []

    # Add input layer
    layers.append(torch.nn.Linear(n_inputs, n_neurons))
    layers.append(torch.nn.ReLU())

    # Add hidden layers
    for _ in range(n_layers):
        layers.append(torch.nn.Linear(n_neurons, n_neurons))
        layers.append(torch.nn.ReLU())

    # Add output layer
    layers.append(torch.nn.Linear(n_neurons, n_outputs))
    layers.append(torch.nn.Softmax(dim=1))

    # Create model
    model = torch.nn.Sequential(*layers)

    return model


def create_optimizer(model, optimizer_type, learning_rate):
    """
    Create an optimizer for a model

    Args:
        model (torch.nn.Sequential): The model to create an optimizer for
        optimizer_type (string): The type of optimizer to create
        learning_rate (float): The learning rate of the optimizer

    Returns:
        torch.optim.Optimizer: The optimizer
    """

    # Create optimizer
    if optimizer_type == "adam":
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    elif optimizer_type == "sgd":
        optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    else:
        raise ValueError(f"Unknown optimizer type: {optimizer_type}")

    return optimizer


def train_model(model, optimizer, epochs, train_data, val_data):
    """
    Train a model

    Args:
        model (torch.nn.Sequential): The model to train
        optimizer (torch.optim.Optimizer): The optimizer to use
        epochs (int): The number of epochs to train for
        train_data (dataframe): The training data
        val_data (dataframe): The validation data

    Returns:
        float: The accuracy of the model on the validation data
    """

    # Separate features and labels
    train_features = train_data.drop(columns=["label"]).to_numpy()
    train_labels = train_data["label"].to_numpy()
    val_features = val_data.drop(columns=["label"]).to_numpy()
    val_labels = val_data["label"].to_numpy()

    # Convert to tensors on GPU
    train_features = torch.tensor(train_features).float().to(device)
    train_labels = torch.tensor(train_labels).to(device)
    val_features = torch.tensor(val_features).float().to(device)
    val_labels = torch.tensor(val_labels).to(device)

    model.to(device)

    # Train model
    for epoch in tqdm(range(epochs)):

        # Forward pass
        train_predictions = model(train_features)
        train_loss = torch.nn.functional.cross_entropy(train_predictions, train_labels.long())

        # Backward pass
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()

    # Evaluate model
    val_predictions = model(val_features)
    correct_predictions = val_predictions.argmax(dim=1) == val_labels
    val_accuracy = correct_predictions.float().mean().item()

    return val_accuracy
