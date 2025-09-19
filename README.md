
## Overview

**Key Features:**
- Weekly kudos allowance (3 per user, resets Monday)
- Organization-scoped kudos (colleagues only)
- Message-based appreciation system
- Real-time updates and history tracking
- Simple user selection interface

**Tech Stack:**
- **Backend:** Django REST Framework, SQLite
- **Frontend:** React with modern hooks and components
- **API:** RESTful endpoints with CORS support

## Project Structure

```
Kudos/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── kudos_backend/         # Django project settings
├── kudos_app/            # Main Django application
│   ├── models.py         # Database models (Organization, User, Kudo)
│   ├── views.py          # API endpoints
│   ├── serializers.py    # DRF serializers
│   └── management/       # Custom commands (demo data generation)
└── kudos_frontend/       # React application
    ├── package.json      # Node.js dependencies
    ├── src/
    │   ├── components/   # React components
    │   ├── api.js        # API service layer
    │   └── App.js        # Main application
```

## Local Development Setup

### Prerequisites
- Python 3.8+ (Python 3.9+ recommended)
- Node.js 16+ and npm
- Git

### Quick Start

1. **Clone and navigate to project:**
   ```bash
   git clone <repository-url>
   cd Kudos
   ```

2. **Backend setup:**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Setup database
   python manage.py migrate
   
   # Generate demo data
   python manage.py generate_demo_data --clear
   
   # Start backend server
   python manage.py runserver 8000
   ```

3. **Frontend setup (in a new terminal):**
   ```bash
   cd kudos_frontend
   npm install
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/


## Demo Data

The application includes pre-generated demo data:
- **4 Organizations** (Company A, B, C, D)
- **15 Users** across organizations
- **Sample kudos** from recent weeks

**Try these demo users:**
- `user1` (Company A) - Has remaining kudos to give
- `user6` (Company B) - Can give kudos to colleagues in Company B
- `user10` (Company C) - Can give kudos to colleagues in Company C

## API Overview

**Key Endpoints:**
- `GET /api/users/me/` - Current user info + remaining kudos
- `GET /api/users/` - Users in same organization
- `POST /api/kudos/` - Give a kudo
- `GET /api/kudos/received/` - Received kudos history

**Authentication:** Simple header-based using `X-User-ID`

**Example API call:**
```bash
curl -X POST "http://localhost:8000/api/kudos/" \
  -H "Content-Type: application/json" \
  -H "X-User-ID: 1" \
  -d '{"receiver": 2, "message": "Great work!"}'
```
