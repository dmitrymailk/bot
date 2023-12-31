# FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel
RUN apt-get update && apt-get upgrade -y 
RUN apt-get install git curl numactl wget -y 

# FROM anibali/pytorch:2.0.1-cuda11.8-ubuntu22.04
# RUN sudo apt-get update && sudo apt-get upgrade -y 
# RUN sudo apt-get install git curl build-essential -y


# RUN chmod -R 777 /root

ARG USERNAME=user-name-goes-here
ARG USER_UID=1001
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    &&  useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
RUN echo -e "\nexport PATH=$PATH:/home/user-name-goes-here/.local/bin\n" >>  /home/user-name-goes-here/.bashrc && sudo chown -R $USERNAME /opt/conda
# I don't know how to do this correct and more stable
RUN pip install ipykernel
WORKDIR /code