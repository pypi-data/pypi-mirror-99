# whatsappy 0.1.6

Whatsappy is a Python library for creating whatsapp bots.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install whatsappy.

```bash
pip install whatsappy-py
```

## Usage

```python
from whatsappy import whatsapp

whatsapp.login() # Login whatsapp

whatsapp.select_chat('Mom') # Goes to the selected chat
whatsapp.send('Hello') # Send a message

whatsapp.exit() # Exit
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](LICENSE)
