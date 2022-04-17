printf "\033[1;31mStarting\033[0m\n"
docker-compose --env-file ./bot/.env build --no-cache && docker-compose --env-file ./bot/.env up -d --force-recreate
