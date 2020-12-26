
# paleolimbot/r-debug

This image is intended for debugging R packages with C or C++ code that aborts R or RStudio unexpectedly. It comes with the latest (as of whenever the image is rebuilt) [devtools](https://devtools.r-lib.org/) installed for convenience. It is intended to be used from the package source directory with the working directory mounted at `/pkg`. This isn't intended to debug specific compilers or errors in dependency packages, but is useful when you're pretty sure that the error is your fault.

``` bash
# docker pull paleolimbot/r-debug
docker run -it --rm -v $(pwd):/pkg paleolimbot/r-debug
```

Inside the container you can install your package and run a command using a debugger. One command that may give you a quick stack trace to your error is `R -d valgrind -e 'mypkg::function_that_crashes_r()'`.

``` bash
R -e 'devtools::install_deps(".", dependencies = TRUE)'
R CMD INSTALL --preclean .
R -d valgrind -e 'mypkg::function_that_crashes_r()'
```

The container comes with a copy of [Davis Vaughan](https://blog.davisvaughan.com)'s [debugit](https://github.com/DavisVaughan/debugit) package mounted at `/pkg` so that you can follow along his [excellent blog post](https://blog.davisvaughan.com/2019/04/05/debug-r-package-with-cpp/) on how to use debuggers in R. 

To use `R -d lldb`, you'll have to relax the security settings for your container with `--security-opt seccomp=unconfined`. This gives the container a lot of power so don't do this unless you need `lldb` and don't use it to run any code that you don't trust!

``` bash
docker run -it --rm --security-opt seccomp=unconfined paleolimbot/r-debug
```
