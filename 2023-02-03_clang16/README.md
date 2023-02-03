
# clang16 / arrow 11.0.0

To build the image (includes installing the arrow package):

```bash
docker build . --tag clang16-arrow
```

To re-run the install/inspect the environment/system:

```bash
docker run --rm -it clang16-arrow bash
# R -e 'install.packages("arrow_11.0.0.tar.gz")'
```
