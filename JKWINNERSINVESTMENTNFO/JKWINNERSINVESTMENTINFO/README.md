# JK Winners Investment Information Management System

Welcome to the JK Winners Investment Information Management System project. This project is designed to provide a comprehensive overview of the JK Winners Investment (JKWI) organization, its structure, divisions, governance, and membership information.

## Project Structure

The project is organized into several directories and files:

- **src/**: Contains the source code for the application.
  - **components/**: Reusable components for the application.
    - `Header.tsx`: Main header component.
    - `Navigation.tsx`: Navigation links component.
    - `CompanyStructure.tsx`: Displays company structure information.
    - `Divisions.tsx`: Presents information about various divisions.
    - `Governance.tsx`: Outlines the governance structure.
    - `Members.tsx`: Showcases information about members.
  - **pages/**: Contains the main pages of the application.
    - `Home.tsx`: Landing page aggregating various components.
    - `Directors.tsx`: Detailed information about the directors.
    - `Divisions.tsx`: Detailed view of the company's divisions.
    - `Membership.tsx`: Information about the membership process.
  - **styles/**: Contains CSS styles for the application.
    - `globals.css`: Global styles for the application.
    - `components.css`: Specific styles for components.
  - **data/**: Contains structured data in JSON format.
    - `company.json`: Information about the company's structure.
    - `divisions.json`: Information about the different divisions.
    - `governance.json`: Information about the governance structure.
  - **utils/**: Utility functions for various operations.
    - `helpers.ts`: Contains helper functions.
  - `App.tsx`: Main application component that sets up routing.

- **public/**: Contains public assets.
  - `index.html`: Main HTML file serving as the entry point.

- **package.json**: Configuration file for npm, listing dependencies and scripts.

- **tsconfig.json**: TypeScript configuration file specifying compiler options.

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the dependencies using npm:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm start
   ```
5. Open your browser and go to `http://localhost:3000` to view the application.

## Contributing

Contributions are welcome! If you would like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.