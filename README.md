# Minecraft Server Starter

> This project is mostly vibecoded.

This project provides a lightweight Python webserver designed to manage the power state of Minecraft server hosts. It integrates with tools like `mc-router` via webhooks to automatically start or stop physical devices based on traffic or demand.


## Features

- **Webhook Integration**: Start/Stop devices via POST requests.
- **Flexible Device Support**: Supports Home Assistant webhooks and (planned) Wake-on-LAN.
- **State Persistence**: Tracks which servers are online and persists this state to disk.
- **Dockerized**: Ready for deployment via Docker and GHCR.

## Setup

### 1. Configuration

Create a `config.yaml` file in the root directory. Define your devices and the servers they host.

```yaml
devices:
  - name: "my-home-server"
    homeassistant:
      webhook: "http://your-ha:8123/api/webhook/unique-id"
    servers:
      - hostname: "survival.example.com"
      - hostname: "creative.example.com"
```

### 2. Home Assistant Setup

If using Home Assistant, you can use the provided `setup/homeassistant_blueprint.yaml` to quickly set up the receiving webhook. Import the blueprint into your Home Assistant instance, provide a unique webhook ID (used in `config.yaml`), and select the switch entity that controls your server's power.

### 3. Running with Docker

In the `setup/` folder there are two docker compose files. One for the router and the other one for the actual server.
Copy them to your servers and modify to your liking (the `docker-compose-server.yml` is basically just a standard `itzg/minecraft-server`)

## Contributing

Contributions are welcome! Whether it's fixing a bug or adding a new feature, feel free to open an issue or submit a pull request.

Potential areas for extension include:
- Support for different webhooks (e.g., for other games).
- Additional methods to start hosts.


