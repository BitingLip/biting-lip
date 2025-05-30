# User Interface (BitingLip Frontend)

This submodule contains the frontend web interface for the BitingLip distributed AI system. It allows users to interact with the system's capabilities, such as submitting inference tasks, viewing results, managing models (via the gateway), and monitoring system status.

## Technology Stack

- **Framework**: Vue.js (version 3 preferred)
- **Build Tool**: Vite
- **State Management**: Pinia (or Vuex)
- **UI Components**: A modern UI library like Vuetify, Quasar, or Tailwind CSS with headless components.
- **Language**: TypeScript (recommended) or JavaScript

## Responsibilities & Planned Features

- **User Authentication**: Secure login and session management, potentially integrating with an auth provider or using API keys managed by the `gateway-manager`.
- **Task Submission**: Forms and interfaces for submitting various AI tasks (e.g., text generation, image generation) to the `gateway-manager` API.
- **Results Display**: Presenting inference results to the user in an intuitive way (text, images, audio).
- **Real-time Updates**: (Optional) Using WebSockets or polling for real-time task status updates and notifications.
- **Model Interaction**: Interface to list available models, view their details, and potentially trigger model downloads or management operations via the `gateway-manager`'s model endpoints.
- **System Monitoring Dashboard**: Displaying key metrics about the cluster, worker status, and API health (data obtained from `gateway-manager` or other monitoring endpoints).
- **Responsive Design**: Ensuring the interface is usable across different devices and screen sizes.

## Getting Started (Development)

### Prerequisites
- Node.js (latest LTS version recommended)
- npm or yarn

### Initial Setup
1.  Navigate to the `user-interface` directory:
    ```bash
    cd user-interface
    ```
2.  Install dependencies:
    ```bash
    npm install
    # or
    # yarn install
    ```
3.  Configure environment variables:
    Create a `.env` file (copied from `.env.example` if it exists) to specify the API endpoint of the `gateway-manager`.
    ```env
    VITE_API_BASE_URL=http://localhost:8080/api/v1 
    # Adjust if your gateway runs elsewhere
    ```

### Running the Development Server
```bash
npm run dev
# or
# yarn dev
```
This will typically start a local development server (e.g., on `http://localhost:5173`).

### Building for Production
```bash
npm run build
# or
# yarn build
```
This will create a `dist/` folder with the optimized static assets for deployment.

## Interaction with Backend

The User Interface primarily interacts with the `gateway-manager`'s REST API to:
- Fetch data (e.g., list of models, task status).
- Submit data (e.g., new inference requests).
- Authenticate users.

## Directory Structure (Typical Vue/Vite Project)

```
user-interface/
├── public/             # Static assets
├── src/
│   ├── assets/         # Images, fonts, etc.
│   ├── components/     # Reusable Vue components
│   ├── views/          # Page components (routes)
│   ├── router/         # Vue Router configuration
│   ├── store/          # Pinia/Vuex store modules
│   ├── services/       # API service wrappers (e.g., Axios instances)
│   ├── App.vue         # Root Vue component
│   └── main.ts         # Main entry point
├── .env.example        # Environment variable template
├── .gitignore
├── index.html          # Main HTML file
├── package.json
├── vite.config.ts      # Vite configuration
└── tsconfig.json       # TypeScript configuration
```

This submodule is currently under development.