FROM fedora:36

RUN dnf install -y cmake g++ ninja-build

RUN mkdir /llvm && \
    curl -L https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.0-rc1.zip \
      -o /llvm.zip && \
    unzip -d /llvm && \
    mv /llvm/`ls /llvm` /llvm/llvm-project
#RUN git clone https://github.com/llvm/llvm-project.git /llvm-project
#RUN cd /llvm-project && git checkout tags/llvmorg-16.0.0-rc1 mkdir build
#RUN cd /llvm-project/runtimes && cmake -G Ninja -S runtimes -B build -DLLVM_ENABLE_RUNTIMES="libcxx;libcxxabi;libunwind" 
#RUN cd /llvm-project/runtimes && ninja -C build cxx cxxabi unwind
#RUN cd /llvm-project/runtimes && ninja -C build check-cxx check-cxxabi check-unwind
#RUN cd /llvm-project/runtimes && ninja -C build install-cxx install-cxxabi install-unwind
