# 🚀 Deployment Guide - EduGenie AI

Complete guide for deploying EduGenie AI to various platforms.

## 📋 Pre-Deployment Checklist

- [ ] All dependencies listed in `requirements.txt`
- [ ] Environment variables configured
- [ ] IBM Cloud API credentials obtained
- [ ] Application tested locally
- [ ] Security settings reviewed
- [ ] Static files optimized

## 🌐 Deployment Options

### 1. IBM Cloud (Recommended)

#### Prerequisites
- IBM Cloud account
- IBM Cloud CLI installed

#### Steps

1. **Install IBM Cloud CLI**
   ```bash
   # Download from: https://cloud.ibm.com/docs/cli
   ```

2. **Login to IBM Cloud**
   ```bash
   ibmcloud login
   ibmcloud target --cf
   ```

3. **Create `manifest.yml`**
   ```yaml
   applications:
   - name: edugenie-ai
     memory: 512M
     instances: 1
     buildpack: python_buildpack
     command: gunicorn app:app
     env:
       FLASK_ENV: production
   ```

4. **Deploy**
   ```bash
   ibmcloud cf push
   ```

5. **Set Environment Variables**
   ```bash
   ibmcloud cf set-env edugenie-ai IBM_CLOUD_API_KEY "your_api_key"
   ibmcloud cf set-env edugenie-ai IBM_WATSONX_PROJECT_ID "your_project_id"
   ibmcloud cf set-env edugenie-ai FLASK_SECRET_KEY "your_secret_key"
   ibmcloud cf restage edugenie-ai
   ```

### 2. Heroku

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps

1. **Create `Procfile`**
   ```
   web: gunicorn app:app
   ```

2. **Create `runtime.txt`**
   ```
   python-3.11.0
   ```

3. **Initialize Git (if not already)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Create Heroku App**
   ```bash
   heroku create edugenie-ai
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set IBM_CLOUD_API_KEY="your_api_key"
   heroku config:set IBM_WATSONX_PROJECT_ID="your_project_id"
   heroku config:set IBM_WATSONX_URL="https://us-south.ml.cloud.ibm.com"
   heroku config:set FLASK_SECRET_KEY="your_secret_key"
   heroku config:set FLASK_ENV="production"
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Open Application**
   ```bash
   heroku open
   ```

### 3. AWS Elastic Beanstalk

#### Prerequisites
- AWS account
- EB CLI installed

#### Steps

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   eb init -p python-3.11 edugenie-ai
   ```

3. **Create Environment**
   ```bash
   eb create edugenie-env
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv IBM_CLOUD_API_KEY="your_api_key" \
            IBM_WATSONX_PROJECT_ID="your_project_id" \
            IBM_WATSONX_URL="https://us-south.ml.cloud.ibm.com" \
            FLASK_SECRET_KEY="your_secret_key" \
            FLASK_ENV="production"
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

6. **Open Application**
   ```bash
   eb open
   ```

### 4. Google Cloud Platform (App Engine)

#### Prerequisites
- GCP account
- gcloud CLI installed

#### Steps

1. **Create `app.yaml`**
   ```yaml
   runtime: python311
   entrypoint: gunicorn -b :$PORT app:app
   
   env_variables:
     FLASK_ENV: 'production'
   
   automatic_scaling:
     min_instances: 1
     max_instances: 3
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

3. **Set Environment Variables**
   ```bash
   gcloud app deploy --set-env-vars IBM_CLOUD_API_KEY="your_api_key",IBM_WATSONX_PROJECT_ID="your_project_id"
   ```

### 5. Azure App Service

#### Prerequisites
- Azure account
- Azure CLI installed

#### Steps

1. **Login to Azure**
   ```bash
   az login
   ```

2. **Create Resource Group**
   ```bash
   az group create --name edugenie-rg --location eastus
   ```

3. **Create App Service Plan**
   ```bash
   az appservice plan create --name edugenie-plan --resource-group edugenie-rg --sku B1 --is-linux
   ```

4. **Create Web App**
   ```bash
   az webapp create --resource-group edugenie-rg --plan edugenie-plan --name edugenie-ai --runtime "PYTHON:3.11"
   ```

5. **Configure Environment Variables**
   ```bash
   az webapp config appsettings set --resource-group edugenie-rg --name edugenie-ai --settings \
     IBM_CLOUD_API_KEY="your_api_key" \
     IBM_WATSONX_PROJECT_ID="your_project_id" \
     FLASK_SECRET_KEY="your_secret_key"
   ```

6. **Deploy**
   ```bash
   az webapp up --name edugenie-ai --resource-group edugenie-rg
   ```

### 6. DigitalOcean App Platform

#### Steps

1. **Connect GitHub Repository**
   - Go to DigitalOcean App Platform
   - Connect your GitHub repository

2. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn app:app`

3. **Set Environment Variables**
   - Add all variables from `.env.example`

4. **Deploy**
   - Click "Deploy"

### 7. Docker Deployment

#### Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

#### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - IBM_CLOUD_API_KEY=${IBM_CLOUD_API_KEY}
      - IBM_WATSONX_PROJECT_ID=${IBM_WATSONX_PROJECT_ID}
      - IBM_WATSONX_URL=${IBM_WATSONX_URL}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - FLASK_ENV=production
    restart: always
```

#### Build and Run

```bash
# Build image
docker build -t edugenie-ai .

# Run container
docker run -p 5000:5000 --env-file .env edugenie-ai

# Or use docker-compose
docker-compose up -d
```

### 8. VPS (Ubuntu/Debian)

#### Steps

1. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python and Dependencies**
   ```bash
   sudo apt install python3 python3-pip python3-venv nginx -y
   ```

3. **Clone Repository**
   ```bash
   git clone <your-repo-url>
   cd "EduGenie AI – Smart Faculty Copilot"
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your credentials
   ```

6. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/edugenie.service
   ```

   ```ini
   [Unit]
   Description=EduGenie AI Application
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/app
   Environment="PATH=/path/to/app/venv/bin"
   ExecStart=/path/to/app/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

7. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/edugenie
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /path/to/app/static;
       }
   }
   ```

8. **Enable and Start Services**
   ```bash
   sudo ln -s /etc/nginx/sites-available/edugenie /etc/nginx/sites-enabled/
   sudo systemctl start edugenie
   sudo systemctl enable edugenie
   sudo systemctl restart nginx
   ```

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit `.env` file
- Use platform-specific secret management
- Rotate API keys regularly

### 2. HTTPS
- Use SSL/TLS certificates
- Enable HTTPS redirect
- Use Let's Encrypt for free certificates

### 3. Rate Limiting
Add to `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

### 4. CORS (if needed)
```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

## 📊 Monitoring

### Application Monitoring
- Use IBM Cloud Monitoring
- Set up error tracking (Sentry)
- Monitor API usage

### Performance Monitoring
- Track response times
- Monitor memory usage
- Set up alerts

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "edugenie-ai"
        heroku_email: "your-email@example.com"
```

## 🧪 Testing Before Deployment

```bash
# Run local tests
python -m pytest

# Test with production settings
FLASK_ENV=production python app.py

# Load testing
pip install locust
locust -f locustfile.py
```

## 📝 Post-Deployment

1. **Verify Deployment**
   - Test all features
   - Check error logs
   - Monitor performance

2. **Update DNS** (if using custom domain)
   - Point domain to deployment
   - Configure SSL

3. **Set Up Backups**
   - Database backups (if applicable)
   - Configuration backups

4. **Documentation**
   - Update deployment docs
   - Document any issues

## 🆘 Troubleshooting

### Common Issues

**Issue**: Application won't start
- Check logs: `heroku logs --tail` or platform equivalent
- Verify environment variables
- Check Python version compatibility

**Issue**: 502 Bad Gateway
- Check if application is running
- Verify port configuration
- Check firewall rules

**Issue**: Slow performance
- Increase worker processes
- Enable caching
- Optimize database queries

## 📞 Support

For deployment issues:
- Check platform documentation
- Review application logs
- Contact platform support

---

**Good luck with your deployment! 🚀**