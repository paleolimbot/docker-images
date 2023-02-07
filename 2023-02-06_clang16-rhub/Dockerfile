FROM rhub/clang16:latest

RUN apt-get update && apt-get install -y cmake git libssl-dev

# Checkout the Arrow + switch to a branch
RUN git clone https://github.com/thisisnic/arrow.git /arrow && \
  cd /arrow && \
  git switch r-11.0.0

RUN mkdir /arrow-build && \
  cd /arrow-build && \
  cmake /arrow/cpp \
  -DCMAKE_C_COMPILER="clang-16"  -DCMAKE_CXX_COMPILER="clang++-16" \
  -DCMAKE_CXX_FLAGS="-stdlib=libc++" \
  -DARROW_CSV=ON -DARROW_DATASET=ON -DARROW_FILESYSTEM=ON \
  -DARROW_COMPUTE=ON -DARROW_PARQUET=ON -DBoost_SOURCE=BUNDLED

# Pass even if the build fails so that we can copy error logs from /arrow-build
ENV VERBOSE 1
RUN cd /arrow-build && cmake --build . > /build_log.txt || true
RUN cp /arrow-build/thrift_ep-prefix/src/thrift_ep-stamp/thrift_ep-build-*.log /
