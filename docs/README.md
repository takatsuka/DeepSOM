## Sphinx Documentation Generation

```bash
cd docs
sphinx-apidoc -f -o source/ ../pysom
make html
```

You should also rename root folder to remove all instances of dashes '-' as
Python does not like importing package names with dashes.

Let's follow the Google Docstring convention, shown here:

https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
