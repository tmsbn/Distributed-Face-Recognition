docker stop $(docker ps -aq)
docker system prune -f
docker image rm autoac
docker image build -t autoac .