# Save Your Money
## Project Description
This is a web application I made in order to keep track of how I'm spending money and how much can I save each month. It's a Python web app that uses Flask for authentication and database management. I used BS4 as HTML and CSS framework for the looks of the web app, a bit of jinja and a bit of JS. For piecharts I used the Google Charts tools.

## Quick Start

### First Time Setup
```bash
./setup.sh
```

### Running the Application
```bash
./run.sh
```

This will automatically:
- Activate the virtual environment
- Set up environment variables
- Run database migrations
- Start the Flask development server

## Manual Installation
1. Clone the repository or download it from GitHub.
2. Open your Terminal of choice and navigate to the repository's folder.
3. Make sure Python3 is installed.
4. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Set environment variables (optional - copy .env.example to .env):
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```
7. Run database migrations (first time only):
   ```bash
   export FLASK_APP=app.py
   flask db upgrade
   ```
8. Start the application:
   ```bash
   python app.py
   ```
9. Open your browser and go to `http://localhost:5000`

## Features
- Supports multiple users, each with it's own personalized data.
![image](https://user-images.githubusercontent.com/59118744/192340301-9779b863-c360-488f-952f-cb862d1ba434.png)
![image](https://user-images.githubusercontent.com/59118744/192343199-7dc4234c-8c09-4292-8902-6cf45e6d5b21.png)

- Keep track of expenses and incomes.
![image](https://github.com/frontman404/save-your-money/assets/59118744/e46046e1-3d0c-4219-a3b8-c0622046fe28")
![image](https://user-images.githubusercontent.com/59118744/192342214-bfea8db9-fbc8-4394-b0f3-643e44d74fd9.png)

- Visualize your data in piecharts.
![image](https://github.com/frontman404/save-your-money/assets/59118744/6e1e76b2-5673-49a7-8c3e-e5e4981a5647")

- Save money to achieve a certain goal.
![image](https://user-images.githubusercontent.com/59118744/192343064-cfcbcdb4-5d50-470d-b670-f94bc8ffd502.png)
![image](https://user-images.githubusercontent.com/59118744/192343412-c7b84875-24a8-4d3c-b6e3-4cebbb391c81.png)

## Development
To run tests:
```bash
python -m pytest tests/
```

### Available Scripts
- `./setup.sh` - Initial project setup (virtual environment, dependencies, database)
- `./run.sh` - Start the development server with automatic migrations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Thanks to Tim from https://www.youtube.com/c/TechWithTim for the inspiration.



