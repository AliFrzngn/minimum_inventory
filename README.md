# Minimum Inventory Management System

A comprehensive, production-ready inventory management system built with modern technologies and best practices.

## 🚀 Features

### Core Functionality
- **Inventory Management**: Complete CRUD operations for inventory items with SKU tracking, barcode support, and category management
- **Stock Control**: Real-time stock level monitoring with low-stock alerts and reorder point management
- **Order Management**: Purchase orders, sales orders, and order tracking with status management
- **Supplier Management**: Comprehensive supplier database with contact information and payment terms
- **User Management**: Role-based access control (Admin, Manager, Staff) with JWT authentication
- **Real-time Updates**: Live stock updates and notifications
- **Reporting**: Comprehensive reports and analytics dashboard

### Technical Features
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Real-time Communication**: WebSocket support for live updates
- **Background Tasks**: Celery for email notifications and report generation
- **Caching**: Redis for session storage and performance optimization
- **Database**: PostgreSQL with Alembic migrations
- **Frontend**: React with TypeScript and modern UI components
- **Monitoring**: Prometheus and Grafana for system monitoring
- **Containerization**: Docker and Docker Compose for easy deployment

## 🏗️ Architecture

### Backend (Core Services)
- **FastAPI**: Primary microservice framework with async support
- **SQLAlchemy**: ORM with Alembic for database migrations
- **PostgreSQL**: Primary database for data persistence
- **Redis**: Caching, session storage, and Celery backend
- **Celery**: Background task processing for notifications and reports
- **Pydantic v2**: Data validation and serialization
- **JWT + OAuth2**: Secure authentication and authorization

### Frontend
- **React 18**: Modern UI framework with hooks and context
- **TypeScript**: Type safety and better developer experience
- **Vite**: Fast build tool and development server
- **TailwindCSS**: Utility-first CSS framework for styling
- **Redux Toolkit**: State management
- **React Query**: Server state management and caching
- **React Router**: Client-side routing

### Infrastructure & DevOps
- **Docker**: Containerization for consistent deployments
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and load balancing
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Visualization and alerting
- **GitHub Actions**: CI/CD pipeline (ready to configure)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd minimum_inventory
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs
   - Grafana Dashboard: http://localhost:3000 (admin/admin)

### Local Development

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp ../env.example .env

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Start Supporting Services
```bash
# Start PostgreSQL and Redis
docker-compose up postgres redis -d

# Start Celery worker (in a separate terminal)
cd backend
celery -A app.core.celery_app worker --loglevel=info
```

## 📊 API Documentation

The API is fully documented with OpenAPI/Swagger. Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - User logout

#### Inventory Management
- `GET /api/v1/inventory/items` - List inventory items
- `POST /api/v1/inventory/items` - Create inventory item
- `GET /api/v1/inventory/items/{id}` - Get specific item
- `PUT /api/v1/inventory/items/{id}` - Update item
- `DELETE /api/v1/inventory/items/{id}` - Delete item
- `POST /api/v1/inventory/items/{id}/adjust-stock` - Adjust stock levels

#### Order Management
- `GET /api/v1/orders` - List orders
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders/{id}` - Get specific order
- `PUT /api/v1/orders/{id}` - Update order
- `PATCH /api/v1/orders/{id}/status` - Update order status

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:password@localhost:5432/inventory_db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-change-in-production` |
| `DEBUG` | Debug mode | `false` |
| `ENVIRONMENT` | Environment name | `development` |

See `env.example` for all available configuration options.

### Database Configuration

The system uses PostgreSQL with the following key tables:
- `users` - User accounts and authentication
- `suppliers` - Supplier/vendor information
- `inventory_items` - Product catalog and stock levels
- `orders` - Purchase and sales orders
- `order_items` - Individual items within orders
- `inventory_updates` - Stock movement history

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Monitoring & Observability

### Metrics
- **Prometheus**: Collects application and system metrics
- **Grafana**: Provides dashboards and alerting
- **Custom Metrics**: Business metrics like inventory levels, order counts

### Logging
- **Structured Logging**: JSON-formatted logs for easy parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Centralized Logging**: Ready for ELK stack integration

### Health Checks
- **Application Health**: `/health` endpoint
- **Database Health**: Connection status monitoring
- **Redis Health**: Cache and session store status

## 🚀 Deployment

### Production Deployment

1. **Set up production environment variables**
2. **Configure SSL certificates**
3. **Set up monitoring and alerting**
4. **Configure backup strategies**
5. **Deploy using Docker Compose or Kubernetes**

### Kubernetes Deployment

The system is designed to be Kubernetes-ready with:
- ConfigMaps for configuration
- Secrets for sensitive data
- Persistent volumes for data
- Ingress for external access
- Horizontal Pod Autoscaling

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Token refresh mechanism

### API Security
- Rate limiting with Nginx
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy

### Infrastructure Security
- Container security best practices
- Network segmentation
- Secret management
- Regular security updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write tests for new features
- Update documentation as needed
- Use conventional commits

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in `/docs`
- Review the API documentation at `/api/docs`

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core inventory management
- ✅ User authentication and authorization
- ✅ Basic reporting and analytics
- ✅ Docker containerization

### Phase 2 (Planned)
- [ ] Advanced reporting with PDF export
- [ ] Mobile application
- [ ] Barcode scanning integration
- [ ] Multi-warehouse support

### Phase 3 (Future)
- [ ] Machine learning for demand forecasting
- [ ] Integration with external systems
- [ ] Advanced analytics and BI
- [ ] Multi-tenant support

---

Built with ❤️ using modern web technologies and best practices.