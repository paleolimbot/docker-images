FROM fedora:36

RUN dnf install -y cmake g++ ninja-build unzip git

# Cloning llvm-project is expensive, so just checkout the version we want
RUN mkdir /llvm && \
    curl -L https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.0-rc1.zip \
      -o /llvm/llvm.zip
RUN unzip /llvm/llvm.zip -d /llvm && \
    rm -f /llvm/llvm.zip && \
    mv /llvm/`ls /llvm` /llvm/llvm-project

RUN cd /llvm/llvm-project &&  \
  cmake -G Ninja -S runtimes -B build -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind"
RUN cd /llvm/llvm-project && ninja -C build cxx cxxabi unwind
RUN cd /llvm/llvm-project && ninja -C build check-cxx check-cxxabi check-unwind
RUN cd /llvm/llvm-project && ninja -C build install-cxx install-cxxabi install-unwind
