# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/14 11:13:09 by xmatute-          #+#    #+#              #
#    Updated: 2025/04/14 13:00:13 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

define ASCIIART

+------------------------+
|   ____  ______  ___    |
|  /    )/      \/   \   |
| (     / __    _\    )  |
|  \    (/ o)  ( o)   )  |
|   \_  (_  )   \ )  /   |
|     \  /\_/    \)_/    |
|      \/  //|  |\\\      |
|          v |  | v      |
|            \__/        |
|                        |
+------------------------+

endef
export ASCIIART

NAME := DB

DOCKER_APP := '/Applications/Docker.app'

SRC_DIR :=	./srcs

DATABASE_DIR := $(SRC_DIR)/database

DCYML := $(SRC_DIR)/docker-compose.yml

WHITE = \033[0;37m
RED = \033[0;31m
CYAN = \033[0;36m
GREEN = \033[0;32m
MAGENTA = \033[0;35m

all : $(DCYML) $(DATABASE_DIR)
	docker compose -f $(DCYML) config
	@echo "making all..."
	docker compose -f $(DCYML) up --build --detach
	@echo "$(MAGENTA)$$ASCIIART$(WHITE)"
	docker ps
	docker volume ls
	docker network ls
	@echo "You can see the database at $(CYAN)http://localhost:8080$(WHITE)"
	@echo "System:		PostgreSQL"
	@echo "Server:		postgres_db"
	@echo "Username:	xmatute-"
	@echo "Password:	mysecretpassword"
	@echo "Database:	piscineds"

$(DATABASE_DIR) :
	mkdir -p $(DATABASE_DIR)

down :
	docker compose -f $(DCYML) down

up :
	docker compose -f $(DCYML) up

reload : down all

clean :
	docker compose -f $(DCYML) down --volumes
	@echo "$(RED)clean done...$(WHITE)"

fclean : clean
	docker system prune --volumes --force --all
	docker container prune --force
	docker volume prune --force
	-docker volume rm $(docker volume ls -q) #puede dar error
	-docker rm -f $(docker ps -a -q) # Elimina todos los contenedores?
	@echo "$(RED)fclean done...$(WHITE)"

re : clean all

hard_re : fclean all

.PHONY : all clean fclean re down up reload