# Production Deployment Guide

This guide provides comprehensive instructions for deploying the Task Manager application to production.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Domain name configured (optional)
- SSL certificate (for HTTPS)

### 1. Environment Configuration

1. Copy the production environment template:
   ```bash
   cp production.env.template .env
   ```

2. Update the `.env` file with your production values:
   ```bash
   # Database Configuration
   project_db_url=mongodb://admin:your_secure_password@mongodb:27017/task_manager_prod?authSource=admin
   DATABASE_NAME=task_manager_prod

   # JWT Configuration - CHANGE THESE IN PRODUCTION
   JWT_SECRET_KEY=your-super-secure-secret-key-here-32-chars-min-change-this-in-production
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Cookie Configuration
   JWT_COOKIE_NAME=access_token
   JWT_COOKIE_DOMAIN=yourdomain.com
   JWT_COOKIE_SECURE=true
   JWT_COOKIE_HTTP_ONLY=true
   JWT_COOKIE_SAME_SITE=strict

   # Application Configuration
   ENVIRONMENT=production
   DEBUG=false
   LOG_LEVEL=INFO

   # CORS Configuration
   FRONTEND_URL=https://yourdomain.com
   ```

### 2. Deploy with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Verify Deployment

- **API Health Check**: `http://your-domain:8000/health`
- **Frontend**: `http://your-domain:3000`
- **API Documentation**: `http://your-domain:8000/docs` (disabled in production)

## 🔧 Manual Deployment

### Backend Deployment

1. **Install Dependencies**:
   ```bash
   uv sync --no-dev
   ```

2. **Set Environment Variables**:
   ```bash
   export ENVIRONMENT=production
   export DEBUG=false
   export project_db_url="your-mongodb-connection-string"
   export JWT_SECRET_KEY="your-secure-secret-key"
   ```

3. **Run Production Server**:
   ```bash
   python main_production.py
   ```

### Frontend Deployment

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm ci --only=production
   ```

2. **Build Application**:
   ```bash
   npm run build
   ```

3. **Start Production Server**:
   ```bash
   npm start
   ```

## 🛡️ Security Checklist

### ✅ Completed Security Measures

- **JWT Authentication**: Secure token-based authentication with HTTP-only cookies
- **Password Hashing**: bcrypt with 12 rounds for password security
- **CORS Configuration**: Properly configured for production domains
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.
- **Input Validation**: Comprehensive Pydantic validation on all endpoints
- **Error Handling**: Secure error responses without sensitive information
- **Database Security**: MongoDB authentication and authorization

### 🔒 Additional Security Recommendations

1. **SSL/TLS**: Use HTTPS in production
2. **Firewall**: Configure proper firewall rules
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Monitoring**: Set up application monitoring and logging
5. **Backup**: Regular database backups
6. **Updates**: Keep dependencies updated

## 📊 Performance Optimizations

### Backend Optimizations

- **Async Operations**: Full async/await support with Beanie ODM
- **Database Indexing**: Automatic index management for optimal queries
- **Connection Pooling**: Efficient database connection management
- **Caching**: Consider implementing Redis for session caching

### Frontend Optimizations

- **Static Generation**: Next.js static optimization
- **Image Optimization**: Optimized logo and asset loading
- **Bundle Optimization**: Tree shaking and code splitting
- **CDN**: Consider using a CDN for static assets

## 🔍 Monitoring and Logging

### Health Checks

- **API Health**: `GET /health` endpoint
- **Database Health**: Automatic connection monitoring
- **Container Health**: Docker health checks configured

### Logging

- **Request Logging**: All API requests logged
- **Error Logging**: Comprehensive error tracking
- **Performance Logging**: Request processing times

## 🗄️ Database Management

### MongoDB Configuration

1. **Authentication**: Enable MongoDB authentication
2. **Replica Set**: Consider setting up replica sets for high availability
3. **Backup Strategy**: Regular automated backups
4. **Monitoring**: Database performance monitoring

### Data Migration

If migrating from development:

```bash
# Export development data
mongodump --db task_manager --out backup/

# Import to production
mongorestore --db task_manager_prod backup/task_manager/
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Check MongoDB connection string
   - Verify network connectivity
   - Check authentication credentials

2. **CORS Issues**:
   - Verify FRONTEND_URL configuration
   - Check allowed origins in CORS middleware

3. **Authentication Issues**:
   - Verify JWT_SECRET_KEY is set
   - Check cookie configuration
   - Ensure HTTPS in production

### Debug Mode

To enable debug mode temporarily:

```bash
export DEBUG=true
export LOG_LEVEL=debug
```

## 📈 Scaling Considerations

### Horizontal Scaling

- **Load Balancer**: Use nginx or similar for load balancing
- **Multiple Backend Instances**: Scale backend containers
- **Database Clustering**: MongoDB replica sets

### Vertical Scaling

- **Resource Limits**: Set appropriate CPU/memory limits
- **Database Optimization**: Index optimization and query tuning
- **Caching Layer**: Implement Redis for session and data caching

## 🔄 Updates and Maintenance

### Application Updates

1. **Backup Database**:
   ```bash
   mongodump --db task_manager_prod --out backup-$(date +%Y%m%d)/
   ```

2. **Update Code**:
   ```bash
   git pull origin main
   docker-compose build
   docker-compose up -d
   ```

3. **Verify Deployment**:
   ```bash
   curl http://your-domain:8000/health
   ```

### Dependency Updates

```bash
# Backend dependencies
uv lock --upgrade

# Frontend dependencies
cd frontend && npm update
```

## 📞 Support

For production support and issues:

1. Check application logs: `docker-compose logs -f`
2. Verify health endpoints: `/health`
3. Review error logs and monitoring
4. Check database connectivity and performance

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificate installed
- [ ] Database authentication enabled
- [ ] Security headers configured
- [ ] Monitoring and logging set up
- [ ] Backup strategy implemented
- [ ] Health checks working
- [ ] Performance optimized
- [ ] Error handling tested
- [ ] Documentation updated
