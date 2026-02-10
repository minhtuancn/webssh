# Deploying Web SSH Terminal on Coolify

<p align="center">
  <img src="https://coolify.io/coolify-logo.png" alt="Coolify Logo" width="200">
</p>

This guide will walk you through deploying Web SSH Terminal on [Coolify](https://coolify.io), a self-hostable Heroku/Netlify alternative.

## Prerequisites

- A Coolify instance (v4.0 or higher recommended)
- A server with at least 1GB RAM
- A domain name (optional, but recommended for production)

## Deployment Methods

Coolify offers multiple ways to deploy Web SSH Terminal. Choose the method that best fits your needs:

### Method 1: Docker Image Deployment (Recommended)

This is the simplest method as it uses the pre-built Docker image.

#### Step 1: Create a New Service

1. Log in to your Coolify dashboard
2. Navigate to your project or create a new one
3. Click **"+ New Resource"** → **"Service"** → **"Docker Image"**

#### Step 2: Configure the Service

**Basic Settings:**
- **Name**: `webssh` (or your preferred name)
- **Image**: `ghcr.io/bifrost0x/webssh:latest`
- **Port**: `5000`

#### Step 3: Set Environment Variables

Click on **"Environment Variables"** and add the following:

**Required Variables:**

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | `<generate-unique-key>` | Generate with: `openssl rand -hex 32` |
| `CORS_ORIGINS` | `https://your-domain.com` | Your Coolify domain or `*` for testing |

**Optional Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `ALLOW_CORS_WILDCARD` | `false` | Set to `true` if using `CORS_ORIGINS=*` |
| `TRUSTED_PROXIES` | `0` | Set to `1` (Coolify uses Traefik proxy) |
| `SESSION_COOKIE_SECURE` | `true` | Keep `true` if using HTTPS |
| `DEBUG` | `False` | Set to `True` only for debugging |
| `HOST` | `0.0.0.0` | Leave as default |
| `PORT` | `5000` | Leave as default |
| `DATA_DIR` | `/app/data` | Leave as default |

**Example Environment Configuration:**
```bash
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
CORS_ORIGINS=https://webssh.yourdomain.com
ALLOW_CORS_WILDCARD=false
TRUSTED_PROXIES=1
SESSION_COOKIE_SECURE=true
```

#### Step 4: Configure Storage

Coolify automatically handles persistent storage, but you can customize it:

1. Go to **"Storage"** tab
2. Add a persistent volume:
   - **Name**: `webssh_data`
   - **Mount Path**: `/app/data`
   - **Type**: Local persistent storage

#### Step 5: Configure Domain

1. Go to **"Domains"** tab
2. Add your domain: `webssh.yourdomain.com`
3. Enable **"Generate Let's Encrypt Certificate"** for HTTPS
4. Enable **"Force HTTPS Redirect"** (recommended)

#### Step 6: Deploy

1. Click **"Deploy"** button
2. Monitor the deployment logs
3. Once deployed, access your Web SSH Terminal at your configured domain

---

### Method 2: Docker Compose Deployment

If you prefer to use Docker Compose or need more control:

#### Step 1: Create a New Service

1. Navigate to your Coolify project
2. Click **"+ New Resource"** → **"Service"** → **"Docker Compose"**

#### Step 2: Paste Docker Compose Configuration

```yaml
services:
  webssh:
    image: ghcr.io/bifrost0x/webssh:latest
    container_name: webssh
    restart: unless-stopped
    environment:
      # Generate with: openssl rand -hex 32
      - SECRET_KEY=${SECRET_KEY}
      
      # Your Coolify domain
      - CORS_ORIGINS=${CORS_ORIGINS}
      
      # Coolify uses Traefik
      - TRUSTED_PROXIES=1
      
      # HTTPS is handled by Coolify
      - SESSION_COOKIE_SECURE=true
      
      # Optional settings
      - ALLOW_CORS_WILDCARD=false
      - DEBUG=False
      - HOST=0.0.0.0
      - PORT=5000
      - DATA_DIR=/app/data
    volumes:
      - webssh_data:/app/data
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.create_connection(('127.0.0.1', 5000), 2); s.close()"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

volumes:
  webssh_data:
    driver: local
```

#### Step 3: Configure Environment Variables

In Coolify, add these environment variables:

```bash
SECRET_KEY=<your-generated-secret-key>
CORS_ORIGINS=https://webssh.yourdomain.com
```

#### Step 4: Configure Domain and Deploy

Follow steps 5-6 from Method 1.

---

### Method 3: GitHub Repository Deployment

Deploy directly from the source code:

#### Step 1: Create a New Application

1. Click **"+ New Resource"** → **"Application"** → **"Public Repository"**
2. Enter repository URL: `https://github.com/bifrost0x/webssh`

#### Step 2: Configure Build Settings

- **Build Pack**: Docker
- **Dockerfile Location**: `/Dockerfile`
- **Port**: `5000`

#### Step 3: Set Environment Variables

Same as Method 1, Step 3.

#### Step 4: Configure Domain and Deploy

Follow steps 5-6 from Method 1.

---

## Post-Deployment Configuration

### 1. Create Your First Account

After deployment:
1. Navigate to your Web SSH Terminal URL
2. Click **"Register"** to create the first account
3. Log in with your credentials

### 2. Test SSH Connection

1. Click **"New Connection"** or use the quick connect form
2. Enter your SSH server details:
   - **Host**: Your server IP or hostname
   - **Port**: SSH port (default: 22)
   - **Username**: Your SSH username
   - **Authentication**: Password or SSH key
3. Click **"Connect"**

### 3. Save Connection Profiles

To save frequently used connections:
1. Go to **Settings** → **Connection Profiles**
2. Add a new profile with your server details
3. Use saved profiles for quick connections

---

## Troubleshooting

### Issue: "CORS Error" in Browser Console

**Solution:**
- Ensure `CORS_ORIGINS` matches your exact Coolify domain
- Include the protocol: `https://webssh.yourdomain.com` (not `webssh.yourdomain.com`)
- If testing locally, you can temporarily set `CORS_ORIGINS=*` and `ALLOW_CORS_WILDCARD=true`

### Issue: "Session Cookie Not Being Set"

**Solution:**
- Verify `TRUSTED_PROXIES=1` is set
- Ensure your Coolify domain has HTTPS enabled
- Check that `SESSION_COOKIE_SECURE=true` (if using HTTPS) or `false` (if using HTTP)

### Issue: "Connection Timeout" When Connecting to SSH Server

**Solution:**
- Check your SSH server is reachable from the Coolify host
- Verify firewall rules allow outgoing SSH connections
- Test SSH connection manually from Coolify host: `ssh user@host -p port`

### Issue: "Application Not Starting"

**Solution:**
1. Check Coolify deployment logs for errors
2. Verify all required environment variables are set:
   - `SECRET_KEY` must be set
   - `CORS_ORIGINS` must be set
3. Check the application logs in Coolify's log viewer

### Issue: "File Upload Fails"

**Solution:**
- Verify the persistent volume is properly mounted at `/app/data`
- Check volume permissions (should be owned by `appuser:appuser`)
- Ensure sufficient disk space on your Coolify host

---

## Security Best Practices

### 1. Use Strong SECRET_KEY

Always generate a unique, cryptographically secure key:

```bash
openssl rand -hex 32
```

Never reuse keys across deployments.

### 2. Enable HTTPS

Coolify makes this easy with Let's Encrypt:
- Always enable "Generate Let's Encrypt Certificate"
- Enable "Force HTTPS Redirect"
- Never use `SESSION_COOKIE_SECURE=false` in production

### 3. Restrict CORS Origins

Use specific domains instead of wildcard:

```bash
# Good for production
CORS_ORIGINS=https://webssh.yourdomain.com

# Bad for production (only use for testing)
CORS_ORIGINS=*
```

### 4. Use Strong Passwords

- Use minimum 8 characters (enforced by application)
- Mix uppercase, lowercase, numbers, and symbols
- Consider using a password manager

### 5. Regular Updates

Keep your deployment up to date:
1. In Coolify, go to your Web SSH service
2. Check for new image versions
3. Update to the latest tag: `ghcr.io/bifrost0x/webssh:latest`
4. Redeploy the service

---

## Backup and Restore

### Backup

Your data is stored in the persistent volume `/app/data`. To backup:

1. **Using Coolify CLI:**
   ```bash
   # SSH into your Coolify host
   docker exec webssh tar -czf /tmp/webssh-backup.tar.gz /app/data
   docker cp webssh:/tmp/webssh-backup.tar.gz ./webssh-backup.tar.gz
   ```

2. **Important files to backup:**
   - `/app/data/webssh.db` - User accounts and settings
   - `/app/data/keys/` - Encrypted SSH keys
   - `/app/data/logs/` - Application logs (optional)

### Restore

1. Stop the Web SSH service in Coolify
2. Restore the backup:
   ```bash
   docker cp webssh-backup.tar.gz webssh:/tmp/
   docker exec webssh tar -xzf /tmp/webssh-backup.tar.gz -C /
   ```
3. Start the service in Coolify

---

## Scaling Considerations

### Resource Requirements

**Minimum:**
- 1 CPU core
- 512 MB RAM
- 1 GB disk space

**Recommended:**
- 2 CPU cores
- 1 GB RAM
- 5 GB disk space

### Performance Tips

1. **Use SSD storage** for the persistent volume
2. **Enable caching** in your reverse proxy
3. **Limit concurrent sessions** if running on limited resources
4. **Monitor resource usage** using Coolify's built-in metrics

---

## Advanced Configuration

### Custom Port Configuration

If you need to change the default port (5000):

1. Update the environment variable:
   ```bash
   PORT=8080
   ```

2. Update the Dockerfile's EXPOSE directive (if building from source)

3. Update Coolify's port mapping

### Behind Additional Reverse Proxy

If running Coolify behind another reverse proxy (e.g., Cloudflare):

1. Set `TRUSTED_PROXIES=1`
2. Ensure WebSocket connections are properly proxied:
   ```nginx
   # Nginx example
   proxy_set_header Upgrade $http_upgrade;
   proxy_set_header Connection "upgrade";
   ```

### Using Custom Themes

The application includes 23 themes by default. Users can select their preferred theme from the UI settings after logging in.

---

## Migration from Other Platforms

### From Docker Compose

1. Export your existing `/app/data` directory
2. Create a new Coolify service using Method 1
3. Before first deployment, upload your data:
   ```bash
   # Copy data to new deployment
   docker cp ./data webssh:/app/data
   ```

### From Kubernetes

1. Export PersistentVolume data
2. Convert environment variables to Coolify format
3. Deploy using Method 1
4. Import your data directory

---

## Support and Resources

### Documentation
- [Main README](README.md) - Overview and features
- [Security Guide](SECURITY.md) - Security best practices
- [Contributing Guide](CONTRIBUTING.md) - Development setup

### Community
- [GitHub Issues](https://github.com/bifrost0x/webssh/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/bifrost0x/webssh/discussions) - Community support

### Coolify Resources
- [Coolify Documentation](https://coolify.io/docs)
- [Coolify Discord](https://coolify.io/discord)

---

## Quick Reference

### Generate SECRET_KEY
```bash
openssl rand -hex 32
```

### Check Logs
In Coolify dashboard → Your Service → Logs tab

### Restart Service
In Coolify dashboard → Your Service → Actions → Restart

### Update to Latest Version
In Coolify dashboard → Your Service → Change image tag to `latest` → Deploy

---

<p align="center">
  <strong>Need help?</strong> Open an issue on <a href="https://github.com/bifrost0x/webssh/issues">GitHub</a>
</p>
