include .env

.PHONY: help
help: # Display this help
	@awk 'BEGIN{FS=":.*#";printf "Usage:\n  make <target>\n\nTargets:\n"}/^[a-zA-Z_-]+:.*?#/{printf"  %-10s %s\n",$$1,$$2}'$(MAKEFILE_LIST)

.PHONY: build
build: # Build service image
	docker build -t $(IMAGE_NAME) .

.PHONY: up
up: build # Start service	 
	docker run -d --restart unless-stopped \
	-e DEBUG=$(DEBUG) -m 1024m \
	--name $(CONTAINER_NAME) -p ${SERVER_PORT}:${SERVER_PORT} $(IMAGE_NAME)

down: # Stop service
	docker rm -f $(CONTAINER_NAME)

logs: # See service logs
	docker logs --tail=100 -f $(CONTAINER_NAME)
