# Real-Time Forest Fire Prediction and Family-Centric Alert System

## 1. Introduction

This project is a real-time forest fire detection, prediction, and alert system designed to protect vulnerable populations, especially the elderly. Inspired by the tragic lessons from recent wildfires, such as the one in Andong, we recognized that standard emergency alerts are often insufficient for those who may not be attentive to them.

Our solution bridges this gap by not only predicting the fire's path but also by directly involving family members in the alert process, ensuring that life-saving information reaches their loved ones effectively.

## 2. Core Features

*   **Real-Time Fire Detection & Spread Prediction**:
    *   Utilizes the **Cell2Fire** simulation engine to generate highly accurate, real-time predictions of a fire's spread.
    *   The system activates the moment a fire is detected.

*   **Dynamic Data Integration**:
    *   Fetches **real-time weather data** upon fire ignition to ensure predictions are based on the most current conditions.
    *   Leverages a pre-processed database of crucial variables, including **mountain terrain data**, fuel types, and other geographical information for enhanced accuracy.

*   **Safe Shelter Guidance**:
    *   Identifies and displays the locations of nearby safety shelters on the map, providing clear evacuation routes.

*   **Family-Centric Alert System**:
    *   This is our key innovation to protect the most vulnerable.
    *   If a registered elderly user is located within the predicted fire spread zone, the system sends an immediate notification to their registered family members.
    *   The alert prompts family members to **personally call** their loved ones, providing a direct, reliable, and reassuring line of communication that is far more effective than a generic alarm.

## 3. How It Works

1.  **Ignition**: A fire is detected.
2.  **Data Fetch**: The system instantly pulls real-time weather data for the affected area.
3.  **Simulation**: It combines the live weather data with our pre-built database (terrain, fuel models) and runs a Cell2Fire simulation.
4.  **Prediction**: A fire spread forecast is generated and visualized on the map as a dynamic risk zone.
5.  **Alert**: The system cross-references the risk zone with the locations of registered users. If a vulnerable user is in danger, their family is immediately alerted to take action.
6.  **Guidance**: All users in the vicinity can view the fire's path and the safest routes to nearby shelters.

## 4. Technology Stack

*   **Backend**: Python (FastAPI)
*   **Frontend**: React.js
*   **Fire Simulation**: Cell2Fire Engine
*   **Mapping Service**: Naver Maps API

## 5. Limitations & Future Work

This project was an ambitious dive into a complex and unfamiliar domain. While we found the challenge both fresh and exciting, we encountered several limitations that also pave the way for future enhancements.

*   **Data Sourcing Challenges**: Our primary limitation was the availability of comprehensive data. The Cell2Fire simulation is powerful, but its accuracy is highly dependent on specific datasets (e.g., detailed fuel models, vegetation types, real-time conditions) that were difficult to acquire for our target region within a limited timeframe. For the demo, we diligently gathered the best available data for a specific mountain near Pohang to showcase the core functionality.

*   **Scalability of Data Handling**: The current version of the Cell2Fire simulation outputs results as CSV files. This approach, while functional for a demo, lacks the scalability and robustness of a proper database system. A key area for future work would be to develop a data pipeline that ingests these CSV outputs into a structured database (e.g., PostgreSQL with PostGIS). This would allow for more complex queries, better data management, and easier integration with other services.

*   **A Meaningful Endeavor**: Despite the challenges, this project was a significant and meaningful learning experience. Within a short period, we successfully navigated a new domain, implemented a complex simulation engine, and built a proof-of-concept that addresses a critical real-world problem. We are proud of the progress made and are confident that this work serves as a strong foundation for a more advanced system in the future.
