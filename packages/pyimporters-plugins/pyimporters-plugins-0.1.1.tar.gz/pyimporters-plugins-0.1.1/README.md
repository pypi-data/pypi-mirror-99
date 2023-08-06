## Setup

- install python3, pip and venv
```
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
```
- create a venv
```
mkdir venv
python3 -m venv venv
source venv/bin/activate
```

- install requirements (inside venv)
```
# Manual install of sklearn
    pip --no-cache-dir --disable-pip-version-check install -r requirements_sklearn.txt

# Manual install of flair
    pip --no-cache-dir --disable-pip-version-check install Pillow==6.2.1 && \
    pip --no-cache-dir --disable-pip-version-check install torch==1.2.0 torchvision==0.4.0 -f https://download.pytorch.org/whl/torch_stable.html && \
    pip --no-cache-dir --disable-pip-version-check install tiny_tokenizer==3.0.1 && \
    pip --no-cache-dir --disable-pip-version-check install deps/flair-0.4.5.1-py3-none-any.whl

# Manual install of delft-0.2.3.5-py3-none-any.whl
    pip --no-cache-dir --disable-pip-version-check install deps/delft-0.2.3.5-py3-none-any.whl && \
    pip --no-cache-dir --disable-pip-version-check install -r requirements.txt && \
    pip --no-cache-dir --disable-pip-version-check uninstall -y tensorflow-gpu && \
    pip --no-cache-dir --disable-pip-version-check install tensorflow==1.12.0

pip install -r requirements.txt
```

- Download spacy models (de, en, fr)7
```
    python3 -m spacy download de && \
    python3 -m spacy download en && \
    python3 -m spacy download fr
```

- launch (single instance)
```
python3 server.py
```


