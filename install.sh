#!/bin/bash

# Download Libsodium
wget https://download.libsodium.org/libsodium/releases/libsodium-stable-2018-04-27.tar.gz || curl https://download.libsodium.org/libsodium/releases/libsodium-stable-2018-04-27.tar.gz

# Untar
tar -zxf libsodium-stable-2018-04-27.tar.gz

# Install
cd libsodium-stable
./configure
make && make check
sudo make install
