FROM debian:bullseye-slim

# Install dependencies
RUN apt-get -qq update; \
    apt-get install -qqy --no-install-recommends \
        gnupg2 wget ca-certificates apt-transport-https \
        autoconf automake cmake dpkg-dev file make patch libc6-dev

# Set repository key
RUN wget -nv -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -

# Install
RUN echo "deb http://apt.llvm.org/bullseye/ llvm-toolchain-bullseye-16 main" \
        > /etc/apt/sources.list.d/llvm.list; \
    apt-get -qq update && \
    apt-get install -qqy -t llvm-toolchain-bullseye-16 clang-16 libc++-16-dev libc++abi-16-dev && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y git r-base cmake libcurl4-openssl-dev libssl-dev

RUN mkdir ~/.R &&  \
  echo 'CXX11=clang++-16 -stdlib=libc++' > ~/.R/Makevars &&  \
  echo 'CXX11STD=-std=c++11' >> ~/.R/Makevars &&  \
  echo 'CXX14=clang++-16 -stdlib=libc++' >> ~/.R/Makevars && \
  echo 'CXX14STD=-std=c++14' >> ~/.R/Makevars &&  \
  echo 'CXX17=clang++-16 -stdlib=libc++' >> ~/.R/Makevars && \
  echo 'CXX17STD=-std=c++17' >> ~/.R/Makevars &&  \
  echo 'CXX20=clang++-16 -stdlib=libc++' >> ~/.R/Makevars && \
  echo 'CXX20STD=-std=c++20' >> ~/.R/Makevars &&  \
  echo 'CXX=clang++-16 -std=c++11  -stdlib=libc++' >> ~/.R/Makevars && \
  echo 'CC=clang-16' >> ~/.R/Makevars

RUN R -e "install.packages(c('cpp11', 'assertthat', 'bit64', 'lifecycle', 'purrr', 'rlang', 'tidyselect', 'vctrs', 'dplyr'))"

COPY arrow_11.0.0.tar.gz /arrow_11.0.0.tar.gz
ENV ARROW_R_DEV=true
RUN R CMD INSTALL arrow_11.0.0.tar.gz
