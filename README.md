# Anime-Recommedation
A REST API service for an Anime Recommendation System that allows users to:
 a)Search for anime by name or genre.
b)View recommended anime based on certain criteria (e.g., popularity, genre match).
c)Authenticate and manage user-specific anime preferences.


# Run the Project:
**1.Clone the repo**
git clone "project-url"
cd anime

**2. Create a Virtual Environment**
python3 -m venv venv
*On Windows*
venv\Scripts\activate
*On macOS/Linux*
source venv/bin/activate


**3. Install Required Dependencies**
pip install -r requirements.txt


**4.Apply Migrations**
python manage.py makemigrations
python manage.py migrate 

**5.Test  API** 
Using tools like Postman.
