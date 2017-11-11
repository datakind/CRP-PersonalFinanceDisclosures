

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t crp-goal3 .

run: ## Run container on port configured in `config.env`
	docker run  -it -p 5000:5000 crp-goal3 


up: build run ## Run container on port configured in `config.env` (Alias to run)

stop: ## Stop and remove a running container
	docker stop crp-goal3;

