#!/bin/bash
cd /usr/local/bin
sudo mkdir ffmpeg && cd ffmpeg
sudo wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
sudo tar -xf ffmpeg-release-amd64-static.tar.xz
sudo ln -s /usr/local/bin/ffmpeg/ffmpeg-5.1.1-amd64-static/ffmpeg /usr/bin/ffmpeg
sudo ln -s /usr/local/bin/ffmpeg/ffmpeg-5.1.1-amd64-static/ffprobe /usr/bin/ffprobe