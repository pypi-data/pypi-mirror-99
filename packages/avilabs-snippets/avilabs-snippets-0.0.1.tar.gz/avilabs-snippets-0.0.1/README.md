# snippets
Grab bag of useful snippets turned into a library.

## To Deploy
```shell

```

## Color Printer
Example
```python
from snippets import color_printer as cp

cp.print_error("This is red.")
cp.print_warn("This is in yellow.")
cp.print_success("This is written in green.")
cp.print_code("This will show up in cyan.")
cp.print_now("Flush this string to stdout without buffering.")
```

## Log Config
Basic Example
```python
configure_logger()
```

Another Example
```python
configure_logger(suppress_noisy_pkgs=["some.noisy.pkg", "another.noisy.pkg"], level=logging.ERROR)
```

## Retry Wrapper
Use this wrapper to automatically add exponential retries to your flaky function.

Example
```python
@retry()
def unpredictable():
    # This will be retried 3 times
    pass
```

Another Example
```python
@retry(max_retries=2)
def unpredictable():
    pass
```