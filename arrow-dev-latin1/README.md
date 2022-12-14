
# Arrow/R development image in the latin-1 locale

This just uses the fact that `docker pull ubunutu:22.04` with `apt-get install r-base` happens to run R in a non-UTF-8 locale. You can update the image to use a different fork/branch to test a PR.

```bash
docker build . --tag arrow-dev-latin1
docker run --rm -it arrow-dev-latin1 bash
```
