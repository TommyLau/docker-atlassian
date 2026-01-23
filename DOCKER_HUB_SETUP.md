# Docker Hub Setup Guide

This guide will help you set up Docker Hub authentication for GitHub Actions to automatically push Docker images.

## Step 1: Create a Docker Hub Access Token

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Click on your username in the top right corner
3. Select **Account Settings**
4. Navigate to **Security** in the left sidebar
5. Click **New Access Token**
6. Give your token a name (e.g., "GitHub Actions")
7. Set permissions to **Read & Write** (or **Read, Write & Delete** if you need to delete images)
8. Click **Generate**
9. **IMPORTANT**: Copy the token immediately - you won't be able to see it again!

## Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click on **Settings** (top menu)
3. Navigate to **Secrets and variables** → **Actions** in the left sidebar
4. Click **New repository secret**
5. Add the following secrets:

   **Secret 1:**
   - Name: `DOCKER_HUB_USERNAME`
   - Value: Your Docker Hub username (e.g., `tommylau`)

   **Secret 2:**
   - Name: `DOCKER_HUB_TOKEN`
   - Value: The access token you created in Step 1

## Step 3: Verify Setup

Once you've added the secrets, the GitHub Actions workflow will automatically:
- Build Docker images when Dockerfiles in level 1 subfolders are changed
- Extract versions from the Dockerfiles
- Tag images with both full version (e.g., `tommylau/bamboo:12.1.0`) and major.minor version (e.g., `tommylau/bamboo:12.1`)
- Push images to Docker Hub

## Manual Trigger

You can also manually trigger the workflow:
1. Go to the **Actions** tab in your GitHub repository
2. Select **Build and Push Docker Images** workflow
3. Click **Run workflow**

## Troubleshooting

### Authentication Errors
- Verify that `DOCKER_HUB_USERNAME` matches your Docker Hub username exactly
- Ensure `DOCKER_HUB_TOKEN` is the correct access token (not your password)
- Check that the token has the correct permissions (Read & Write)

### Version Extraction Errors
- Ensure your Dockerfile follows this pattern:
  - `FROM atlassian/<product>:<version>` (e.g., `FROM atlassian/bamboo:12.1.0`)

### Build Errors
- Check that the base images exist (e.g., `atlassian/bamboo:12.1.0`)
- Verify that all URLs in the Dockerfile are accessible
- Check the Actions logs for detailed error messages
