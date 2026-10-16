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

If using Home Assistant, you can use the provided `homeassistant_blueprint.yaml` to quickly set up the receiving webhook. Import the blueprint into your Home Assistant instance, provide a unique webhook ID (used in `config.yaml`), and select the switch entity that controls your server's power.

### 3. Running with Docker

Build and run the container:

```bash
docker build -t mc-server-starter .
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/config.yaml:/data/config.yaml \
  -v $(pwd)/state.yaml:/data/state.yaml \
  mc-server-starter
```

## Integration with mc-router

To use this with `mc-router`, configure the router's webhook settings to target the `/scale` endpoint of this server.

**Request Format:**
- **Method**: `POST`
- **URL**: `http://<starter-ip>:5000/scale`
- **Body (JSON)**:
  ```json
  {
    "action": "up", 
    "serverAddress": "survival.example.com",
    "backend": "10.0.0.5:25565"
  }
  ```

**Logic:**
- `action: "up"`: If no servers on the host are currently online, the starter triggers the device's "up" mechanism (e.g., Home Assistant webhook).
- `action: "down"`: If the requested server is the last one online on the host, the starter triggers the device's "down" mechanism.

## Contributing

Contributions are welcome! Whether it's fixing a bug or adding a new feature, feel free to open an issue or submit a pull request.

Potential areas for extension include:
- Support for different webhooks (e.g., for other games).
- Additional methods to start hosts.


