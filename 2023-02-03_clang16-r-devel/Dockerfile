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

ENV CRAN http://cran.r-project.org

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	        bison \
		ca-certificates \
		curl \
		debhelper \
		default-jdk \
		ghostscript \
		groff-base \
		less \
		libblas-dev \
		libbz2-dev \
		libcairo2-dev \
		libcurl4-openssl-dev \
		libicu-dev \
		libjpeg-dev \
		liblapack-dev \
		liblzma-dev \
		libncurses5-dev \
		libpango1.0-dev \
		libpcre2-dev \
		libpng-dev \
		libreadline-dev \
		libtiff5-dev \
		libx11-dev \
		libxt-dev \
		lmodern \
		locales \
		mpack \
		qpdf \
		subversion \
		tcl8.6-dev \
		texinfo \
		texlive-base \
		texlive-extra-utils \
		texlive-fonts-extra \
		texlive-fonts-recommended \
		texlive-plain-generic \
		texlive-latex-base \
		texlive-latex-extra \
		texlive-latex-recommended \
        tidy \
		tk8.6-dev \
		valgrind \
		unzip \
		x11proto-core-dev \
		xauth \
		xdg-utils \
		xfonts-base \
		xfonts-100dpi \
		xfonts-75dpi \
		xvfb \
		zlib1g-dev \
        cmake

RUN apt-get install -y --no-install-recommends fonts-texgyre

RUN curl -o /usr/bin/pandoc.gz \
         https://files.r-hub.io/pandoc/linux-64/pandoc.gz && \
    gzip -d /usr/bin/pandoc.gz && \
    curl -o /usr/bin/pandoc-citeproc.gz \
	 https://files.r-hub.io/pandoc/linux-64/pandoc-citeproc.gz && \
    gzip -d /usr/bin/pandoc-citeproc.gz && \
    chmod +x /usr/bin/pandoc /usr/bin/pandoc-citeproc

RUN apt-get install -y aspell aspell-en rsync gfortran

RUN cd /tmp \
    && svn co https://svn.r-project.org/R/trunk R-devel

ENV RPREFIX /opt/R-devel

ENV ROPTIONS --with-recommended-packages --enable-R-shlib --enable-R-static-lib

## Configure default locale,
## see https://github.com/rocker-org/rocker/issues/19
RUN echo "en_US.ISO-8859-15 ISO-8859-15" >> /etc/locale.gen && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen &&             \
    locale-gen en_US.ISO-8859-15 &&                            \
    locale-gen en_US.UTF-8 &&                                  \
    /usr/sbin/update-locale LANG=en_US.ISO-8859-15             \
    /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.iso885915
ENV LANG en_US.iso885915

RUN cd /tmp/R-devel \
    && ./tools/rsync-recommended \
    && R_PAPERSIZE=letter                                    \
    R_BATCHSAVE="--no-save --no-restore"                     \
    PERL=/usr/bin/perl                                       \
    R_UNZIPCMD=/usr/bin/unzip                                \
    R_ZIPCMD=/usr/bin/zip                                    \
    R_PRINTCMD=/usr/bin/lpr                                  \
    AWK=/usr/bin/awk                                         \
    CFLAGS="-Wall -pedantic"                      \
    CXXFLAGS="-Wall -pedantic"                               \
    LIBS="-lz -lbz2 -llzma"                                  \
    CC="clang-16"                                               \
    CXX="clang++-16 -stdlib=libc++"                                            \
    ./configure --prefix=${RPREFIX} ${ROPTIONS}              \
    && make                                                  \
    && make install

RUN /opt/R-devel/bin/R -e "install.packages(c('cpp11', 'assertthat', 'bit64', 'lifecycle', 'purrr', 'rlang', 'tidyselect', 'vctrs', 'dplyr'), repos = 'https://cloud.r-project.org')"

RUN mkdir ~/.R &&  \
  echo 'CXX11STD=-std=c++11' > ~/.R/Makevars &&  \
  echo 'CXX14STD=-std=c++14' >> ~/.R/Makevars &&  \
  echo 'CXX17STD=-std=c++17' >> ~/.R/Makevars &&  \
  echo 'CXX20STD=-std=c++20' >> ~/.R/Makevars &&  \
  echo 'CXX=clang++-16 -std=c++11  -stdlib=libc++' >> ~/.R/Makevars && \
  echo 'CC=clang-16' >> ~/.R/Makevars

COPY arrow_11.0.0.tar.gz /arrow_11.0.0.tar.gz
ENV ARROW_R_DEV=true
RUN /opt/R-devel/bin/R CMD INSTALL arrow_11.0.0.tar.gz
