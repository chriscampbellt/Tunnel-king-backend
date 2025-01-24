# Tunnel King

The AI Service Manager is a desktop and web-based solution designed to manage model servers, user interactions, and configurations. It allows administrators to oversee model deployments, user permissions, and live updates while providing an intuitive user interface for interacting with models.

# Setup Instructions
install make and docker, docker-compose

copy env file and set the required env accordingly
```bash

copy ./config/env/.env.example .env
```
build
```bash
make dev.build
```
run app
```
make dev.up
```
open new terminal and apply migrations
```bash

make dev.migrate
```

# License

This project is licensed under the MIT License.

# Contributions

Contributions are welcome! Please open an issue or submit a pull request for any improvements or fixes.
