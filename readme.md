# Game Download Time Calculator

This web application calculates the estimated download time for various popular games based on user-inputted download speed.

## Features

- Calculates download time in seconds, minutes, hours, or days depending on the size of the game and user's download speed.
- Allows sorting of games by download time.
- Dark-themed UI with a blueish color scheme.
- Responsive design for desktop and mobile browsers.

## Technologies Used

- **Backend:** Python with Flask
- **Frontend:** HTML, CSS (styled with a dark theme)
- **JavaScript:** Fetch API for asynchronous communication
- **Deployment:** Flask's built-in development server

## Setup Instructions

To run this application locally, follow these steps:

1. **Clone Repository:**
   ```bash
   git clone https://github.com/iLeaksy/GameTime-App.git
   cd GameTime-App
   ```

2. **Install Dependencies:**
   Ensure you have Python installed. Then, install Flask:
   ```bash
   pip install Flask
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```
   Open your web browser and go to `http://127.0.0.1:5000/` to view the application.

## Usage

1. Enter your upload and download speeds in Mbps.
2. Click on the "Calculate" button to see the estimated download times for various games.
3. Click on "Sort by Download Time" button to sort the games from fastest to slowest download times.

## Screenshots

![Screenshot 1](/screenshots/screenshot1.png)
![Screenshot 2](/screenshots/screenshot2.png)



