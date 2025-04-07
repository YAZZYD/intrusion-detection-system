# Intrusion Detection System

This is an Intrusion Detection System (IDS) designed to detect and classify network intrusions.

## 📌 Description

This project processes network capture files (`.pcap`) to extract relevant features, preprocesses them, and then applies machine learning models to classify different types of attacks.

## 📥 Dataset

The dataset used for this project is the [IoT Network Intrusion Dataset](https://ieee-dataport.org/open-access/iot-network-intrusion-dataset). Download it from the provided link and place the `.pcap` files without the need of the description file (`.csv`) since its already there in the `datasets/` directory.

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/YAZZYD/intrusion-detection-system.git
cd intrusion-detection-system
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## 🔨 Usage

You can use the provided `Makefile` to easily run different parts of the project.

```bash
make train-with-pre-processed                # Run the script with preprocess dataset
make train             # Run the script without preprocess dataset (read directly from csv)
make cache-clear                           #clear '__pycache__' (you can use pyclean if python3.8+)
make test-model                            # test the model with given dataset
```
