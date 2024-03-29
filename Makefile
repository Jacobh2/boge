
start-rpi:
	docker compose up --build -d app --remove-orphans


start-home:
	docker run -d \
		--name homeassistant \
		--privileged \
		--restart=unless-stopped \
		-e TZ=Europe/Stockholm \
		-v /home/jacobhagstedt/projects/boge/home_assistant_config:/config \
		-v /run/dbus:/run/dbus:ro \
		--network=host \
		ghcr.io/home-assistant/home-assistant:stable

start:
	docker compose -f docker-compose-home.yaml up -d

kill-all:
	docker stop -t 1 $(docker ps -aq)
	docker rm $(docker ps -aq)

