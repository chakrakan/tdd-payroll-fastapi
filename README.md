# Payroll System

![Continuous Integration and Delivery](https://github.com/chakrakan/tdd-payroll-fastapi/workflows/Continuous%20Integration%20and%20Delivery/badge.svg?branch=main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A sample payroll processing application built using FastAPI to demonstrate my skills for production/near production!

Feedback is welcome and you can provide them by directlly creating [gh-issues](https://github.com/chakrakan/tdd-payroll-fastapi/issues) on the repo.

## 1. Instructions on how to build/run your application

#### Deployed Instance

This API and PostgresDB is deployed on a free Heroku dyno - visit [here](https://cryptic-peak-99939.herokuapp.com/docs) to interact with the API directly from the Swagger UI specs without installing anything locally!

```text
P.S. free Dyno's are by default asleep after 30 mins of inactivity and will require a cold start for the first request, so I highly suggest visiting the docs page first to "boot" up the dyno before hitting the other endpoints
```

Routes

https://cryptic-peak-99939.herokuapp.com/docs - to access auto-generated OpenAPI 3 docs to test out below endpoints without a Front-end interface!  
https://cryptic-peak-99939.herokuapp.com/v1/health - simple `GET` endpoint for health check  
https://cryptic-peak-99939.herokuapp.com/v1/upload - csv_file `POST` upload route  
https://cryptic-peak-99939.herokuapp.com/v1/report - `GET` request to retrieve report of all uploaded data

#### 🐳 Docker

This app is fully Dockerized (API and DB for test, and dev), thus the fastest way to get setup locally is:
- directly pulling the final image hosted as a package on Github: https://github.com/chakrakan/tdd-payroll-fastapi/packages/905453

or 

- using the `docker-compose.yml` file supplied. Ensure you have Docker and docker cli tools installed on your local machine

You can always clone the repo, make a virtualenv manually and `pip install -r requirements-dev.txt` to install dev+main deps and run the project via a direct call to `uvicorn app.main:app --reload --workers 4 --host 0.0.0.0 --port 8000` from the `payroll/` folder, but that's far less exciting 😆

The API container is referred as `payroll` and the PgSQL DB container is `payroll-db` with tables `payroll_dev` and `payroll_test`.

Steps for local docker method:

1. Clone the repository locally
2. `cd` to the root of the project where `docker-compose.yml` resides
3. Run `docker-compose up -d --build` to build the images and containers
4. Once the containers are up and running, upgrade DB to provided aerich migrations using `docker-compose exec payroll aerich upgrade`
5. You can check `docker-compose exec payroll-db psql -U postgres` followed by `\c payroll_dev` and then `\dt` to ensure the tables have been created
6. Feel free to test out the endpoints using your method of choice (Postman/Insomnia/cURL etc.) or you can directly use Swagger UI at `http://localhost:8004/docs` to test out the entire API visually!

Additional Commands:

Lint code: `docker-compose exec payroll python -m flake8 .`
Format code-check: `docker-compose exec payroll python -m black . --check`
Sort dependencies: `docker-compose exec payroll python -m isort .`

Routes

http://localhost:8004/docs - to access auto-generated OpenAPI 3 docs to test out below endpoints without a Front-end interface!  
http://localhost:8004/v1/health - simple health check  
http://localhost:8004/v1/upload - csv_file post upload route  
http://localhost:8004/v1/report - get request to retrieve report

Features (Basic functionality++):

- Leverage Pipenv for managing and separating dev/prod dependecies akin to a Rust `cargo.toml` setup
- Leverage TDD which is native to FastAPI using PyTest
- Utilize an async ORM to manage DB interactions
- Leverage FastAPI auto-documentation features to adhere to OpenAPI specs with a Swagger UI to test out endpoints
- Leverage modern Python features (3.9+) such as asyncio, type declarations
- Dockerized API and DB for multiple environments (dev/test/prod)
- CI/CD via Github Workflows which builds, tests, and deploys our docker images

## 2. Answers to the following questions

- **How did you test that your implementation was correct?**  
  **A.** This API was built using TDD w/ `pytest` while leveraging Python (3.9+) features such as types and pythonic async-await. There were some nifty edge cases that I was able to circumvent due to this and add custom responses based on the scenario! You can run the tests using `docker-compose exec payroll python -m pytest`. Apart from that, I also tested the endpoints directly via Postman to ensure correct upload behavior/report generation.

- **If this application was destined for a production environment, what would you add or change?**  
  **A.** Lots more testing - specifically using asyncio pytest to test out my async methods within the api/services.py file since as you can see based on the codecov report:
  <p align="center">
   <img src="https://github.com/chakrakan/tdd-payroll-fastapi/blob/main/docs/coverage.png" width="400" alt="Codecov report" /></a>
  </p>
  I could've done better 😅
  
  I'd also use an async task queue like Celery to better optimize large file uploads and processing in the background. Current implementation uses 4 uvicorn workers (feel free to increase this number by editing `uvicorn` workers to `2 * no. of CPU cores + 1` processes) to parallelly process the file in FastAPI's BackgroundTasks - a basic non-blocking Task queue implementation. The file itself is also chunked in memory as a SpooledTemporaryFile, where once the `fileno()` is triggered, it'll be automatically stored to the `tmp/` drive and read as needed. For production, I'd use something like a Dask dataframe to handle reading huge CSV files in memory-constrained cloud VMs which does most of these processes internally in one line of code 🤯

  An async ORM, Tortoise-ORM is being leveraged with the `asyncpg` adapter for PostgreSQL to achieve [maximum performance](https://github.com/tortoise/orm-benchmarks#quick-analysis) for DB interactions.

  Almost all operations within the code-base are at worst case O(N), with the most taxing jobs of filtering and searching being done in O(logN) time on the PgSQL DB, and the report generation being O(NM) due to `.extend` on the array, but can be optimized further to use a dictionary and made O(N+M) and can still be linear.

  I'd also change the CORS policy to better adhere and restrict access to the endpoints as necessary instead of allowing all.

  While there is a CI/CD pipeline that runs the tests in a test env, I'd also add does security scanning of containers/dependecies for prod + have a proper branching setup (dev, main, features, bug branches etc.) with rules for PR reviews/merge conditions prior to production deployments.

  Happy to receive additional feedback to further learn more about ways to optimize my solution for the challenge and for prod! 😊

- **What compromises did you have to make as a result of the time constraints of this challenge?**  
   **A.** I'm quite happy with the implementation I have made within the time constraints! If I didn't have other interviews/obligations, I'd probably write more tests and figure out the async pytest integration to test out the services individually. add Celery and Dask to the project. However, for the purposes, I didn't want to over-engineer the solution as I like the philoshopy at Wave where we try to write robust code without introducing technical debt, but at the same time, iterate and continuosly make things better!

  I know I did not have to do all the setups/configs for this project to the level I did, but I wanted to use this not just to do ANOTHER take home project, but also leverage this as a great learning experience for me as well, since I've never worked with FastAPI and its underlying eco-system (Tortoise-ORM, aerich etc.) and also am a bit rusty with my Python and any new features since (last used 3.7 or so). All in all, it was extremely fun to through all the documentation and resources to put together, time spent debugging code, and put something together in a few hours over the weekend!

  If you'd like to see my full thought-process, feel free to dive further into the [Wiki!](https://github.com/chakrakan/tdd-payroll-fastapi/wiki)

  Thank you for the opportunity!

  -- [Kanisk](https://kanisk.live/)

### Miscellaneous

#### Folder structure

`tree -I '__pycache__|htmlcov|*.csv'`

```bash
.
├── README.md
├── docker-compose.yml
├── docs
│   └── coverage.png
├── payroll
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── aerich.ini
│   ├── app
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── generate_report.py
│   │   │   ├── health_check.py
│   │   │   ├── services.py
│   │   │   └── upload.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── models
│   │       ├── __init__.py
│   │       ├── pydantic.py
│   │       └── tortoise.py
│   ├── db
│   │   ├── Dockerfile
│   │   └── create.sql
│   ├── entrypoint.sh
│   ├── migrations
│   │   └── models
│   │       └── 0_20210719154333_init.sql
│   ├── requirements-dev.txt
│   ├── requirements.txt
│   ├── setup.cfg
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_api_services.py
│       ├── test_generate_report.py
│       ├── test_health.py
│       ├── test_upload.py
│       └── wave-logo.png
└── release.sh
```
