# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the Minimum Inventory Management System. These workflows provide comprehensive CI/CD, code quality checks, security scanning, and automated deployment.

## 📋 Workflows Overview

### 1. **CI/CD Pipeline** (`.github/workflows/ci.yml`)
**Triggers:** Push to main/develop, Pull Requests
**Purpose:** Main continuous integration pipeline

**Features:**
- ✅ Backend tests with PostgreSQL and Redis services
- ✅ Frontend tests and linting
- ✅ Security scanning (Bandit, Safety, Semgrep)
- ✅ Docker build testing
- ✅ Integration tests
- ✅ Code quality gates
- ✅ Coverage reporting with Codecov

**Services:**
- PostgreSQL 15
- Redis 7
- Full test environment setup

### 2. **Code Quality** (`.github/workflows/code-quality.yml`)
**Triggers:** Push to main/develop, Pull Requests
**Purpose:** Comprehensive code quality analysis

**Features:**
- ✅ Python code formatting (Black)
- ✅ Import sorting (isort)
- ✅ Linting (Flake8)
- ✅ Type checking (MyPy)
- ✅ Security linting (Bandit)
- ✅ Dependency vulnerability scanning (Safety)
- ✅ Frontend linting (ESLint)
- ✅ TypeScript checking
- ✅ Console log detection
- ✅ TODO comment tracking

### 3. **Security Scan** (`.github/workflows/security.yml`)
**Triggers:** Push to main/develop, Pull Requests, Weekly schedule
**Purpose:** Comprehensive security vulnerability scanning

**Features:**
- ✅ Python security scanning (Bandit, Safety)
- ✅ Node.js security scanning (npm audit)
- ✅ Container security scanning (Trivy)
- ✅ CodeQL analysis
- ✅ Dependency review for PRs
- ✅ Snyk security scanning (optional)
- ✅ SARIF upload to GitHub Security tab

### 4. **Deploy** (`.github/workflows/deploy.yml`)
**Triggers:** Push to main, Manual dispatch
**Purpose:** Automated deployment to staging and production

**Features:**
- ✅ Docker image building and pushing to GHCR
- ✅ Multi-environment deployment (staging/production)
- ✅ Health checks after deployment
- ✅ Rollback capabilities
- ✅ Deployment notifications
- ✅ Manual deployment triggers

### 5. **Dependency Updates** (`.github/workflows/dependency-update.yml`)
**Triggers:** Weekly schedule, Manual dispatch
**Purpose:** Automated dependency management

**Features:**
- ✅ Python dependency updates
- ✅ Node.js dependency updates
- ✅ Security vulnerability detection
- ✅ Automatic PR creation for updates
- ✅ Security issue creation for vulnerabilities

### 6. **Performance Tests** (`.github/workflows/performance.yml`)
**Triggers:** Push to main/develop, Pull Requests, Weekly schedule
**Purpose:** Performance and load testing

**Features:**
- ✅ Load testing with custom scripts
- ✅ Memory profiling
- ✅ Database performance testing
- ✅ Lighthouse CI for frontend performance
- ✅ Performance regression detection
- ✅ PR comments with performance metrics

### 7. **Release** (`.github/workflows/release.yml`)
**Triggers:** Git tags, Manual dispatch
**Purpose:** Automated release management

**Features:**
- ✅ Automatic changelog generation
- ✅ Release creation with artifacts
- ✅ Docker image tagging
- ✅ Release notifications
- ✅ Prerelease detection

## 🔧 Configuration

### Required Secrets

Add these secrets to your GitHub repository settings:

```bash
# Optional - for enhanced security scanning
SNYK_TOKEN=your_snyk_token

# Optional - for notifications
SLACK_WEBHOOK_URL=your_slack_webhook
DISCORD_WEBHOOK_URL=your_discord_webhook
```

### Environment Variables

The workflows use these environment variables:

```yaml
PYTHON_VERSION: '3.11'
NODE_VERSION: '18'
POSTGRES_VERSION: '15'
```

### Service Dependencies

Several workflows require external services:
- **PostgreSQL 15** - For database testing
- **Redis 7** - For caching and session testing
- **Docker** - For containerization testing

## 📊 Monitoring and Reporting

### Coverage Reports
- Backend coverage is uploaded to Codecov
- Frontend coverage is generated locally
- Coverage thresholds are enforced

### Security Reports
- Bandit reports for Python security
- Safety reports for dependency vulnerabilities
- npm audit reports for Node.js security
- Trivy reports for container security
- CodeQL analysis for code security

### Performance Metrics
- Load testing results
- Memory usage profiling
- Database performance metrics
- Lighthouse performance scores

## 🚀 Usage

### Running Workflows Manually

1. **Code Quality Check:**
   ```bash
   # Triggered automatically on PRs
   # Or manually via GitHub Actions tab
   ```

2. **Security Scan:**
   ```bash
   # Runs weekly automatically
   # Or manually via GitHub Actions tab
   ```

3. **Deploy to Staging:**
   ```bash
   # Triggered on push to main
   # Or manually via GitHub Actions tab
   ```

4. **Create Release:**
   ```bash
   # Create a git tag
   git tag v1.0.0
   git push origin v1.0.0
   
   # Or manually via GitHub Actions tab
   ```

### Workflow Status

All workflows include status checks that:
- ✅ Block merging if tests fail
- ✅ Require code quality approval
- ✅ Enforce security standards
- ✅ Validate performance metrics

## 🔍 Troubleshooting

### Common Issues

1. **Tests Failing:**
   - Check service dependencies (PostgreSQL, Redis)
   - Verify environment variables
   - Review test logs for specific errors

2. **Security Scan Failures:**
   - Review security reports
   - Update dependencies with vulnerabilities
   - Fix code security issues

3. **Deployment Issues:**
   - Check deployment environment configuration
   - Verify Docker image builds
   - Review deployment logs

4. **Performance Test Failures:**
   - Check performance thresholds
   - Review load test results
   - Optimize slow queries or operations

### Debug Mode

To enable debug logging, add this to workflow steps:
```yaml
- name: Debug
  run: |
    echo "Debug information"
    # Add debug commands
  env:
    ACTIONS_STEP_DEBUG: true
```

## 📈 Metrics and KPIs

The workflows track these key metrics:

- **Test Coverage:** > 80% for backend, > 70% for frontend
- **Security Score:** No high-severity vulnerabilities
- **Performance:** < 2s response time, > 10 RPS
- **Code Quality:** All linting checks pass
- **Deployment Success:** > 95% success rate

## 🔄 Maintenance

### Regular Tasks

1. **Weekly:**
   - Review dependency updates
   - Check security scan results
   - Monitor performance metrics

2. **Monthly:**
   - Update workflow dependencies
   - Review and optimize test performance
   - Update security scanning rules

3. **Quarterly:**
   - Review and update workflow configurations
   - Evaluate new security tools
   - Optimize CI/CD pipeline performance

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Buildx Documentation](https://docs.docker.com/buildx/)
- [CodeQL Documentation](https://codeql.github.com/)
- [Lighthouse CI Documentation](https://github.com/GoogleChrome/lighthouse-ci)

---

**Note:** These workflows are designed to be production-ready and follow security best practices. Always review and customize them according to your specific requirements and security policies.

