# Flask Image Converter
This is a test project created in 2024. Its purpose is to convert uploaded images to the WebP format using the Flask web framework and the Pillow library. This project also helped me learn continuous deployment using Docker, GitHub Actions, and Google Cloud Run. The image converter functionality is aimed at supporting other projects by efficiently handling image conversion needs without the needs of credits.
## Technologies used
<div align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E"/>
  <img src="https://img.shields.io/badge/Github%20Actions-282a2e?style=for-the-badge&logo=githubactions&logoColor=367cfe"/>
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white"/>
</div>

## Getting started
To run this Flask image converter application locally, follow these steps:
**1. Clone this repository**
```bash
git clone https://github.com/your-username/flask-image-converter.git
cd flask-image-converter
```
**2. Set up a virtual environment and install dependencies:**
```
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
**3. Run the development server:**
```
flask run
```
**4. Open the application in your browser**
Visit http://localhost:5000 to access the image converter interface.

## Deployment
The application is designed to be deployed using Docker and managed through GitHub Actions for CI/CD. It can be easily deployed to Google Cloud Run for scalable, serverless deployment.

- Docker: Containerize the application for consistent and isolated environments.
- GitHub Actions: Automate the deployment pipeline.
- Google Cloud Run: Run the application in a scalable, serverless environment.

## Icons used
[Badges4Readme](https://github.com/alexandresanlim/Badges4-README.md-Profile) - alexandresanlim
