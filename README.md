# Security Camera Docker Container

This repository contains a Docker-based security camera application.

## Prerequisites

- Docker and Docker Compose installed on your system
- USB camera connected to your system (mounted at `/dev/video0`)

## Getting Started

### Building the Container

To build the container, run: 

```bash
docker-compose build
```

You'll know the build is successful when you see:
- No error messages in red
- A "Successfully built" message at the end
- The image appears when you run `docker images`

If you see any errors during the build process, check:
- Your Dockerfile syntax
- Network connectivity for downloading packages
- System requirements and permissions

### Starting the Container

To start the security camera container:

```bash
docker-compose up -d
```

The `-d` flag runs the container in detached mode (background).

### Stopping the Container

To stop the running container:

```bash
docker-compose down
```

### Viewing Logs

To view the container logs:

```bash
docker-compose logs -f security-camera
```

The `-f` flag follows the log output in real-time.

## Configuration

### Docker Configuration
- Timezone set to Europe/London
- Access to USB camera at `/dev/video0`
- Captured images are stored in the `./images` directory
- Container automatically restarts unless explicitly stopped

### Telegram Configuration
The application uses telegram-send to notify about motion detection. The configuration file must be located at:
- Project directory: `~/docker/security-camera/telegram-send.conf`
- Inside container: `/root/.config/telegram-send.conf`

⚠️ Important: 
- Keep your `telegram-send.conf` file secure as it contains your Telegram bot token
- This file is excluded from git via `.gitignore`
- The file must be in the project directory (same location as Dockerfile)

If you need to reconfigure Telegram:
1. Enter the container: `docker exec -it security-camera bash`
2. Run: `telegram-send --configure`
3. Copy the config out: `docker cp security-camera:/root/.config/telegram-send.conf ./telegram-send.conf`
4. Rebuild the container: `docker-compose build`
5. Restart: `docker-compose up -d`

## Volume Mounts

- `.:/app` - Mounts the entire directory for development
- `./images:/app/images` - Persists captured images

## Notes

- The container runs with privileged access which may be required for camera functionality
- Ensure your USB camera is properly connected and accessible at `/dev/video0` 