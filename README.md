# Energy Management Dashboard

<p align="center">
  <img width="400" alt="Screenshot 2024-11-05 at 16 10 28" src="https://github.com/user-attachments/assets/7435e66a-4515-418e-8838-d735cdc2c5d1">
  <img width="400" alt="Screenshot 2024-11-05 at 16 10 39" src="https://github.com/user-attachments/assets/eec29ec6-d8f1-444d-98a4-7a8878a3b396">
  <img width="400" alt="Screenshot 2024-11-05 at 16 10 48" src="https://github.com/user-attachments/assets/70c81435-c73f-44a2-a4ad-b035201372ff">
</p>

## Overview

The Energy Management Dashboard is a web-based application that provides a comprehensive and interactive visualization of energy consumption data. The dashboard allows users to explore and analyze energy usage patterns, identify trends, and gain insights into energy efficiency opportunities. An <a href="https://energy-app-j53xm.ondigitalocean.app/">example</a> of the app is hosted on Digital Ocean.

## Features

* **Real-time data visualization**: The dashboard displays real-time energy consumption data, allowing users to monitor energy usage in real-time.
* **Interactive charts and graphs**: Users can interact with charts and graphs to explore energy usage patterns, identify trends, and gain insights into energy efficiency opportunities.
* **Customizable dashboards**: Users can input custom data to display data available to them by simply editing the api file and changing the list of available measurements in the assets folder.

## Technical details

* **Built with Dash**: The Energy Dashboard is built using Dash, a Python framework for building web applications.
* **Data sources**: The dashboard uses data from sources, including energy meters. This can be configured via a custom api (from an industrial historian for instance).

## Directory structure

```
├── Dockerfile
├── app
│   ├── __init__.py
│   ├── api
│   ├── assets
│   ├── callbacks
│   ├── config
│   ├── layouts
│   └── utils
└── requirements.txt
```

## Measurements

The `tag_list.csv` file is a critical component of the app, as it defines the measurement tags used in the app. Each row in the file represents a single measurement tag, with the following columns (example of tags below):

| id | name | group | tag | process |
|----|------|-------|-----|---------|
| 14 | Warehouse Forklift 1 | Logistics | WF_1 | Material Handling |
| 15 | Warehouse Forklift 2 | Logistics | WF_2 | Material Handling |
| 24 | Conveyor Belt System | Material Handling | CBS_1 | Material Handling |
| 28 | Robotic Arm | Automation | RA_1 | Material Handling |
| 0 | Assembly Line A | Production | AL_A | Assembly |
| 1 | Assembly Line B | Production | AL_B | Assembly |

* **tag**: The name of the measurement tag.
* **name**: A brief description of the measurement tag.
* **process**: The process from which the measurement belongs. Used for categorization.

This file can be edited with available measurements. The tag column is used to query data from the API where the full tag format is `tag` + `_` + `sensor #`. The sensors can be configured in the config file.

## How to Run the Code

1. Build docker image:
   ```
   docker build -t dashapp .
   ```

2. Run docker image:
   ```
   docker run -p 8051:8051 dashapp
   ```
   
3. Access dashboard:
   ```
   http://0.0.0.0:8051
   ```
   
## Credits

## License

This project is licensed under the [License Name] - see the [LICENSE.md](LICENSE.md) file for details.
