

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t crp-goal3 .

run: ## Run container on port configured in `config.env`
	docker run  -v $(shell pwd):/usr/src/app -it -p 8080:8080 crp-goal3 


up: build run ## Run container on port configured in `config.env` (Alias to run)

stop: ## Stop and remove a running container
	docker stop crp-goal3;

