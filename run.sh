gnome-terminal -e "docker run --rm -it -e SYSTEM_TYPE=server facerek"
gnome-terminal -e "docker run -p 5001:5000 --rm -it -e SYSTEM_TYPE=node facerek"
