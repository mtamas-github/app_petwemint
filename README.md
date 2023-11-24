# APP Petwemint

Managing photo gallery, generating digital art from photos using python photo manipulation libraries and neural art. Creating NFT from digital art and sell it through checkout.

### Django features
- User management (login, register, etc)
- checkout, payments
### App features
- special user gallery with secure upload 
- generating art - multiple different methods
- generate NFT
- downloadable content

<br />


## ✨ Start the app in Docker

> `Note`: Make sure you are in the root of the project. 

```bash
$ docker-compose up --build 
```

Visit `http://localhost:85` in your browser. The app should be up & running.



### 👉 Set Up for `Unix`, `MacOS` 

> Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
Copy env.sample to .env and set up database details

<br />

> Migrate Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

### 👉 Set Up for `Windows` 

> Install modules via `VENV` (windows) 

```
$ virtualenv env
$ .\env\Scripts\activate
$ pip3 install -r requirements.txt
```

<br />
Copy env.sample to .env and set up database details

> Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

### 👉 Create Users

By default, the app redirects guest users to authenticate. In order to access the private pages, follow this set up: 

- Access the `registration` page and create a new user:
  - `http://127.0.0.1:8000/register/`
- Access the `sign in` page and authenticate
  - `http://127.0.0.1:8000/login/`

<br />


