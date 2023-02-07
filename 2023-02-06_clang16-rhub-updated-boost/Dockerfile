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

RUN apt-get install -y rsync
RUN cd /arrow/r && make sync-cpp && cd .. && R CMD build r
RUN R -e 'install.packages("pak")' && R -e "pak::local_install_deps('/arrow/r')"
ENV VERBOSE 1
ENV ARROW_R_DEV true
RUN R CMD INSTALL /arrow/arrow_11.0.0.tar.gz
RUN R -e 'library(arrow)'
