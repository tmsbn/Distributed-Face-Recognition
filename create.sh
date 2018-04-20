docker stop $(docker ps -aq)
docker system prune -f
docker image rm facerek
docker image build -t facerek .