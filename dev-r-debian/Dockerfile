FROM debian:testing

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Halifax
RUN apt-get update && \
    apt-get install -y \
    # General development tools
    locales gdb gcc g++ valgrind r-base cmake git \
    # Needed for tidyverse + devtools install
    libxml2-dev libcurl4-openssl-dev libssl-dev libgit2-dev libfontconfig1-dev libfreetype6-dev libharfbuzz-dev libfribidi-dev libpng-dev libtiff5-dev libjpeg-dev

# Generate a UTF-8 locale and make sure R uses it
RUN locale-gen en_CA.UTF8 && update-locale en_CA.UTF8 && \
    echo 'invisible(Sys.setlocale("LC_ALL", "en_CA.UTF8"))' > ~/.Rprofile

# Install rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Set default R repos
RUN echo 'options(repos = c("CRAN" = "https://cloud.r-project.org"))' > ~/.Rprofile

# Use more than one processor for compilation
ENV NUM_PROC 7
RUN mkdir ~/.R && echo 'MAKEVARS = -j${NUM_PROC}' > ~/.R/Makevars

# Install a bunch of R packages
RUN R -e 'install.packages("pak")'
RUN R -e 'pak::pkg_install(c("tidyverse", "devtools", "nycflights13"), dependencies = TRUE)'

# dev setup
RUN mkdir /rscratch
RUN git config --global user.name "Dewey Dunnington"
RUN git config --global user.email "dewey@dunnington.ca"

# Arrow development environment
RUN git clone https://github.com/paleolimbot/arrow.git /rscratch/arrow && \
  cd /rscratch/arrow && \
  git remote add upstream https://github.com/paleolimbot/arrow.git && \
  git pull upstream master
ENV ARROW_BUILD /rscratch/arrow-build
ENV ARROW_HOME /rscratch/arrow-dist
ENV ARROW_SOURCE /rscratch/arrow
ENV ARROW_R_DEV true
ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:${ARROW_HOME}/lib
COPY arrow-build.sh /rscratch/arrow-build.sh

# Install R dependencies for Arrow
RUN R -e 'pak::local_install_dev_deps(file.path(Sys.getenv("ARROW_SOURCE"), "r"))'

# Run the build once so there's always a recent-ish Arrow build on hand
RUN rscratch/arrow-build.sh
