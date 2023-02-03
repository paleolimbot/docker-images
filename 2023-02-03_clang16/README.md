
# clang16 / arrow 11.0.0

Based on imagess at https://github.com/silkeh/docker-clang .

As of this writing, the clang version is

```
root@b3f003d14d84:/# clang++ --version
Debian clang version 16.0.0 (++20230116071901+2563ad8ef1a8-1~exp1~20230116072002.532)
Target: x86_64-pc-linux-gnu
Thread model: posix
InstalledDir: /usr/bin
```

To build the image (includes installing the arrow package):

```bash
docker build . --tag clang16-arrow
```

To re-run the install/inspect the environment/system:

```bash
docker run --rm -it clang16-arrow bash
# R -e 'install.packages("arrow_11.0.0.tar.gz")'
```
