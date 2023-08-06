# Boydem - Simple Persistent Python Storage

## What is it good for?
* Debugging multiple sessions in parallel.
* Keep objects between interpreter session.
* Storing random objects for using later.

## What is this name "boydem"?
It's Attic in Yiddish 😊

## Install

```console
pip install boydem
```

## Usage

```python
>>> from boydem import boydem

>>> boydem
Nothing here 😳

>>> boydem.a = 3

>>> boydem[123] = {"key": "val"}

>>> boydem
a: 3
123: {'key': 'val'}

>>> "a" in boydem
True

>>> 123 in boydem
True

>>> "bla" in boydem
False

>>> len(boydem)
2

>>> for key, val in boydem:
...     print(f"{key}: {val}")
...
a: 3
123: {'key': 'val'}

>>> boydem.keys()
dict_keys(['a', 123])

>>> boydem.values()
dict_values([3, {'key': 'val'}])

>>> boydem.items()
dict_items([('a', 3), (123, {'key': 'val'})])

>>> boydem.clear()
Nothing here 😳

>>> boydem.is_it_here = True

>>> exit()

$ python
Python 3.8.0 ...
>>> from boydem import boydem

>>> boydem
is_it_here: True
```

## Development

```console
git clone https://github.com/omrirz/boydem.git
cd boydem
pip install -r requirements.txt
```

## Test

```console
tox
```
