printf "\033[1;31mStarting\033[0m\n"
docker-compose build && docker-compose up -d --force-recreate
