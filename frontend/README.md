# Task Manager Frontend

A modern Next.js frontend application for the Task Manager system, built with React, Tailwind CSS, and integrated with a FastAPI backend.

## Features

- **Authentication**: JWT-based authentication with HTTP-only cookies
- **Task Management**: Full CRUD operations for tasks with filtering and sorting
- **User Management**: Admin interface for managing users
- **Dashboard**: Statistics and overview of tasks
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark Mode**: Automatic dark mode based on system preference
- **Real-time Updates**: Context-based state management

## Tech Stack

- **Framework**: Next.js 15
- **Language**: JavaScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **HTTP Client**: Axios
- **Forms**: React Hook Form
- **Date Handling**: date-fns
- **Authentication**: HTTP-only cookies

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   ├── layouts/           # Layout components
│   ├── pages/             # Next.js pages (routing)
│   ├── styles/            # Global styles
│   ├── hooks/             # Custom React hooks
│   ├── utils/             # Helper functions
│   ├── context/           # Context API providers
│   ├── services/          # API service layer
│   ├── middleware/        # Authentication middleware
│   ├── config/            # Configuration files
│   └── constants/         # Constant values
├── .env.local             # Environment variables
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── jsconfig.json          # Path aliases
└── package.json           # Dependencies
```

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Running FastAPI backend on http://localhost:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env.local
```

3. Update `.env.local` with your backend URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors

## API Integration

The frontend communicates with the FastAPI backend through:

- **Authentication**: `/auth/*` endpoints
- **Tasks**: `/tasks/*` endpoints  
- **Users**: `/users/*` endpoints

All API calls use HTTP-only cookies for authentication and include proper error handling.

## Key Features

### Authentication
- Login/Register forms with validation
- JWT token management via HTTP-only cookies
- Protected routes with middleware
- Automatic token refresh

### Task Management
- Create, read, update, delete tasks
- Filter by status, priority, labels, due date
- Task statistics dashboard
- Real-time status updates

### User Management
- User listing with search
- Create/edit user profiles
- Activate/deactivate users
- User task assignments

### UI/UX
- Responsive design for all screen sizes
- Dark mode support
- Loading states and error handling
- Form validation with helpful messages
- Accessible components

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Deploy to Other Platforms

The built application can be deployed to any platform that supports Node.js:
- Netlify
- AWS Amplify
- Railway
- DigitalOcean App Platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.