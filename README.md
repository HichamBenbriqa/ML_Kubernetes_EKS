# Deploying a Machine Learning Model with Flask, Gunicorn, and Kubernetes on AWS EKS

This project demonstrates how to deploy a machine learning model using Flask and Gunicorn as a web service endpoint, and then serve it using Kubernetes specifically in AWS EKS. The production-ready model is fetched from Neptune.AI model registry and served via Flask application (app.py). The endpoint is tested using the requests library from Python.

## Prerequisites

- Python 3.x installed on your machine
- Docker installed on your machine
- Access to AWS EKS (Amazon Elastic Kubernetes Service) cluster
- Neptune.AI account with the model tagged as 'PRODUCTION' in the model registry

## Setup

1. Clone this repository:

```bash
git clone git@github.com:HichamBenbriqa/ML_Kubernetes_EKS.git
cd your-project
```
    Install the required Python packages:

```bash
poetry install
```

    Set up your Neptune.AI credentials by exporting them as environment variables:

```bash
export NEPTUNE_API_TOKEN='your-neptune-api-token'
export NEPTUNE_PROJECT_NAME='your-neptune-project-name'
```
    Run the Flask application to serve the model:

```bash
python app.py
```

Testing

    Ensure that the Flask application is running.
    Run the provided test script to test the endpoint:

```bash

python test_endpoint.py
```

Containerization and Deployment

    Dockerize the Flask application:

```bash
docker build -t your-docker-image-name .
docker run -p 8001:8001 -it image-id
```
    Push the Docker image to Docker Hub or AWS ECR:

```bash
# For Docker Hub
docker tag your-docker-image-name your-dockerhub-username/your-docker-image-name
docker push your-dockerhub-username/your-docker-image-name

# For AWS ECR
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-aws-account-id.dkr.ecr.your-region.amazonaws.com
docker tag your-docker-image-name your-aws-account-id.dkr.ecr.your-region.amazonaws.com/your-docker-image-name
docker push your-aws-account-id.dkr.ecr.your-region.amazonaws.com/your-docker-image-name
```
    Deploy the Docker image to AWS EKS:

```bash
# Create Kubernetes deployment
kubectl apply -f deployment.yaml

# Expose deployment as a service
kubectl expose deployment your-deployment-name --type=LoadBalancer --port=8000 --target-port=8000

# Get the external IP address
kubectl get svc
```
