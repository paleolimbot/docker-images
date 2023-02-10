FROM debian:testing

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Halifax
RUN apt-get update && \
    apt-get install -y \
    # General development tools
    locales gdb gcc g++ valgrind r-base cmake git curl nano python3-pip \
    # Needed for tidyverse + devtools install
    libxml2-dev libcurl4-openssl-dev libssl-dev libgit2-dev libfontconfig1-dev libfreetype6-dev libharfbuzz-dev libfribidi-dev libpng-dev libtiff5-dev libjpeg-dev

# Install OSGeo stack
RUN apt-get update && apt-get install -y libudunits2-dev libgdal-dev libgeos-dev libproj-dev

# Generate a UTF-8 locale and make sure R uses it
RUN sed -i '/en_CA.UTF-8/s/^# //g' /etc/locale.gen && \
  locale-gen && \
  update-locale en_CA.UTF-8 && \
  echo 'invisible(Sys.setlocale("LC_ALL", "en_CA.UTF-8"))' >> ~/.Rprofile
ENV LANG en_CA.UTF-8 
ENV LANGUAGE en_CA:en 
ENV LC_ALL en_CA.UTF-8

# Install rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rustup.sh && \
  chmod +x rustup.sh && \
  ./rustup.sh -y && \
  rm -f rustup.sh

# Set default R repos
RUN echo 'options(repos = c("CRAN" = "https://cloud.r-project.org"))' >> ~/.Rprofile

# Use more than one processor for compilation
ENV NUM_PROC 7
RUN mkdir ~/.R && \
  echo 'MAKEVARS = -j${NUM_PROC}' > ~/.R/Makevars

# For arm64 (i.e., Docker on M1) we need -fPIC not -fpic
RUN dpkg --print-architecture | grep -e arm64 && \
  echo 'CFLAGS += -fPIC' >> ~/.R/Makevars && \
  echo 'CXX11FLAGS += -fPIC' >> ~/.R/Makevars && \
  echo 'CXX14FLAGS+= -fPIC' >> ~/.R/Makevars && \
  echo 'CXX17FLAGS+= -fPIC' >> ~/.R/Makevars && \
  echo 'CXX20FLAGS+= -fPIC' >> ~/.R/Makevars && \
  echo 'CXXFLAGS += -fPIC' >> ~/.R/Makevars

# Install a bunch of R packages
RUN R -e 'install.packages("pak")'
RUN R -e 'pak::pkg_install(c("tidyverse", "devtools", "nycflights13"), dependencies = TRUE)'

# Install the dev dependencies for all the packages I maintain
RUN R -e 'pak::pkg_install(c("edwards97", "exifr", "geos", "ggspatial", "libgeos", "mudata2", "prettymapr", "rcanvec", "rosm", "tidypaleo", "wk", "wkutils"), dependencies = TRUE)'

# Install a bunch of Python packages
RUN pip3 install pyarrow jupyter

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
ENV LD_LIBRARY_PATH ${ARROW_HOME}/lib:${LD_LIBRARY_PATH}
COPY arrow-build.sh /rscratch/arrow-build.sh

# Install (most) R dependencies for Arrow
RUN R -e 'pak::pkg_install(setdiff(desc::desc_get_deps(file.path(Sys.getenv("ARROW_SOURCE"), "r"))$package, c("stats", "R")))'

# Run the build once so there's always a recent-ish Arrow build on hand
RUN /rscratch/arrow-build.sh

WORKDIR /rscratch
