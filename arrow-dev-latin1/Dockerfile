FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Halifax
RUN apt-get update && apt-get install -y gcc-12 g++-12 valgrind r-base cmake git libxml2-dev libcurl4-openssl-dev libssl-dev libgit2-dev libfontconfig1-dev libfreetype6-dev libharfbuzz-dev libfribidi-dev libpng-dev libtiff5-dev libjpeg-dev
RUN R -e 'install.packages(c("testthat", "pkgbuild", "cpp11", "R6", "assertthat", "bit64", "bit", "cli", "ellipsis", "glue", "magrittr", "purrr", "rlang", "blob", "stringr",  "tidyselect", "vctrs", "lubridate", "dplyr", "hms"), repos = "https://cloud.r-project.org")'
RUN git clone https://github.com/apache/arrow.git /arrow && mkdir /arrow-build && cd /arrow-build && cmake /arrow/cpp -DARROW_CSV=ON -DARROW_DATASET=ON -DARROW_FILESYSTEM=ON -DARROW_COMPUTE=ON -DARROW_PARQUET=ON -DBoost_SOURCE=BUNDLED && cmake --build . && cmake --install . --prefix /arrow-dist
ENV ARROW_HOME /arrow-dist
ENV LD_LIBRARY_PATH /arrow-dist/lib

# Generate a non-UTF-8 locale and make sure R uses it
RUN apt-get install -y locales && locale-gen en_CA && update-locale en_CA && echo 'invisible(Sys.setlocale("LC_ALL", "en_CA"))' > ~/.Rprofile

# Checkout a different fork/commit of the arrow R package. Works as long as this is
# pretty close to apache/arrow@master but is useful to test the difference between branches
# without having to rebuild arrow

# for master
# RUN git clone https://github.com/apache/arrow.git /arrow-r && cd /arrow-r && git switch master

# for a PR
RUN git clone https://github.com/paleolimbot/arrow.git /arrow-r && cd /arrow-r && git switch r-path-latin1

RUN cd /arrow-r/r && R CMD INSTALL .
