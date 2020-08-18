# apexofficeprint-python
This project provides a Python interface for APEX Office Print.

## Contributing

### Useful VS Code extensions
- `njpwerner.autodocstring`: Python docstring generator, uses Google-style docs by default.

### pdoc
[pdoc](https://pdoc3.github.io/pdoc/) is used for documentation generation.
Things to keep in mind when writing docs (some of these are non-standard):
- Docstrings are inherited from `super()`.
- Instance variables (attributes) can have docstrings, start the docstring on the line *underneath* the attribute
- For `@property` properties, the setter's documentation is ignored. Make sure everything is in the getter.
