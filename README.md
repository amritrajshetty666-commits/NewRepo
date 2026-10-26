# DevOps Orders CI/CD Lab

A local DevOps project for practising Git, Jenkins, Docker,
automated testing, and Kubernetes deployments.

## Architecture

- Frontend: HTML served by Nginx
- Backend: Python FastAPI orders API
- Database: PostgreSQL
- Reverse proxy: Nginx
- Container orchestration: Kubernetes (kind)
- CI/CD: Jenkins

## Planned pipeline

1. Commit and push code to Git.
2. Jenkins checks out the repository.
3. Run Python checks and unit tests.
4. Build a versioned Docker image.
5. Load the image into the local kind cluster.
6. Deploy the application to Kubernetes.
7. Verify rollout and application health.

## Local development

The Docker Compose configuration is available in `docker-compose.yml`.
