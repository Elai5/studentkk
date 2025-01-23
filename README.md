# StudentKonect

StudentKonnect is a social media platform tailored for foreign students navigating life in a new country. Imagine a Kenyan student in Canada who wants to connect with other Kenyan students nearby—whether at the same school, city, or town. This app bridges that gap, fostering a support network while providing real-time insights into local transportation, cultural norms, and housing options. It simplifies integration and enhances connections, helping students feel at home in unfamiliar environments.


   ## Table of Contents

1. [About StudentKonnect](#about-studentkonnect)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Future Enhancements](#future-enhancements)
7. [Contributing](#contributing)
8. [License](#license)

# About StudentKonnect
Relocating to a foreign country as a student can be daunting. From cultural shock to logistical challenges like housing, transportation, and social networking, the transition often lacks proper support. StudentKonnect addresses these challenges by offering:

- A Support Network: Connects students based on geolocation, institution, and personal interests.

- Localized Insights: Provides real-time news on transportation, local food, cultural norms, and academic resources.

-Easy Communication: Facilitates seamless interactions through features like real-time messaging and friend requests.

- StudentKonnect empowers students to thrive by fostering connections and providing essential tools to navigate their new environment with ease.

## Features

1. **User Authentication & Profile Management**:  
   - Secure sign-up and login process using OTP validation.  
   - Profile customization with personal details like country, institution, and city.

2. **Real-Time Communication**:  
   - Real-time messaging and friend requests for seamless student networking.

3. **Location-Based Resources**:  
   - Real-time updates on transportation, food, cultural norms, and academic resources based on user location.

4. **Cultural Integration**:  
   - Features aiding students in adapting to new environments through cultural insights and networking.

5. **Event and Networking Opportunities**:  
   - Event discovery and participation for academic and social networking.


## Run Locally  

1. Clone the project

```bash

  git clone <repository-url>  
 ```

2. Create a virtual environment:
```bash
    python -m venv env  
    source env/bin/activate (Linux/Mac) or env\Scripts\activate (Windows)  
```
3. or activate the current virtual env
```bash
 source env/bin/activate .venv   (Linux/Mac)
  or env\Scripts\activate .venv (Windows)  
```
4. Go to the project directory
```bash
  cd studentkonnect 
```
5. Install dependencies

```bash
  pip install -r requirements.txt  

```
6. set up the database
```bash
    python manage.py makemigrations  
    python manage.py migrate  

```
7. Start the server

```bash
  python manage.py runserver  

```

8. Access the app at http://localhost:8000

## Tech Stack 

**Client:** Client-Side
HTML, CSS, JavaScript, Bootstrap,

**Server:** Django
Python, APIs


## Future-enhancements
1. Upcoming Features:

- Events Page: A platform for students to discover and participate in academic, social, and networking events based on their location.
- Post Page: A space where students can share survival tips, advice, and stories to help others adapt.
- Native Student Sign-Up: Allowing native students to join and mentor foreign students.
2. Improvements:

- Enhancing real-time messaging for better performance and user experience.
- Optimizing user profiles for additional customization options.



## Documentation

[Documentation](https://linktodocumentation)


## Environment Dependancies

To run this project, you will need to add the following environment Dependancies

To set up and run StudentKonnect, you’ll need to configure the following environment variables. Ensure you have Python 3, Django, and a virtual environment set up.

1. Python Version
- Ensure Python 3.x is installed on your system.
- Example: Python 3.8+
2. Django

- Django should be installed for backend development.
- Example: django>=3.0
3. Virtual Environment
- Create a virtual environment for the project.
Example:
``` bash
    python3 -m venv venv
    source venv/bin/activate  # For Unix/Linux/Mac
    venv\Scripts\activate  # For Windows

```

