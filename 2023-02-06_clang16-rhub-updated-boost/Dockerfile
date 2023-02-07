FROM rhub/clang16:latest

RUN apt-get update && apt-get install -y cmake git libssl-dev

# Checkout the Arrow + switch to a branch
RUN git clone https://github.com/thisisnic/arrow.git /arrow && \
  cd /arrow && \
  git switch r-11.0.0

RUN git config --global user.email "you@example.com" && \
  git config --global user.name "Your Name"

# pick the boost fix
RUN cd /arrow && \
  git remote add paleolimbot https://github.com/paleolimbot/arrow.git && \
  git fetch paleolimbot && \
  git switch update-bundled-boost && \
  git switch r-11.0.0 && \
  git cherry-pick 964488a66fa89a5818589910be06eaa55e485370 && \
  git cherry-pick 654afce44ece22b2c5a84e62bb46d4cf0f256aa3 && \
  git cherry-pick ddc5c78dd722eb8068a9eae9ce5ae07c954ae2e3 && \
  git cherry-pick a934a4806e3d7972cc9b42f737615369ba1599c0

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
RUN cp /arrow-build/thrift_ep-prefix/src/thrift_ep-stamp/thrift_ep-build-*.log / || true
