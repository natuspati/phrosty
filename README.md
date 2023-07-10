[![LinkedIn][linkedin-shield]][linkedin-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/natuspati/phrosty">
    <img src=phrosty-frontend/src/assets/img/logo.png alt="Logo" width="200" >
  </a>

<h3 align="center">Phrosty</h3>

  <p align="center">
    Freelance cleaning service.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Game</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#Running tests">Changes to Front-end</a></li>
        <li><a href="#screenshots">Changes to Back-end</a></li>
      </ul>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project

Phrosty is a full-stack project that aims to build a freelance cleaning service similar to Uber, Lyft.

The primary workflow is
* A user (_client_) creates a request for a cleaning with a give date, location and price.
* Cleaning request is available publicly and other users (_cleaners_) can offer to accept the request.
* When client approves one of the offers, the remaining offers are rejected.
* Selected cleaner may cancel the offer anytime, thus making the request available again.
* After the request is satisfied, the client may leave a review of the cleaner. The reviews are aggregated for each
user and available publicly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

#### Back-end

Back-end is built with FastAPI using Test Driven Development.

* Pytest is chosen for its mature resources and extensive ecosystem of plugins.
* Validation and ORM use Pydantic models.
* SQL queries are written in pure SQL for speed. 
* Permissions, authorization and pagination are configured with dependencies. 

#### Front-end

Front-end is built with React and Elastic-UI.

* React-router is used for front-end navigation.
* React-redux manages the state.
* Custom hooks are used to create a simple apiClient and connect authorization with back-end resources.

[![FastAPI][fastapi.com]][fastapi-url]
[![React][React.js]][React-url]
[![ElasticUI][ElasticUI.com]][ElasticUI-url]
[![React Router][ReactRouter.com]][ReactRouter-url]
[![React Redux][ReactRedux.com]][ReactRedux-url]
[![Docker][Docker.com]][Docker-url]
[![PostgreSQL][PostgreSQL.com]][PostgreSQL-url]
[![Redis][Redis.com]][Redis-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

For the front-end, make sure `yarn` is installed.

For the backend, Docker and docker-compose must be installed. See here installation instructions:
[Get Docker](https://docs.docker.com/get-docker/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/natuspati/country-guess-game.git
   ```
2. Install packages for the front-end
   ```sh
   yarn --cwd phrosty-frontend install
   yarn --cwd phrosty-frontend start
   ```
3. Spin up `docker-compose` containers in a new terminal
   ```sh
   docker-compose -f docker-compose.yml up -d --build
   ```
4. Make migrations using alembic
   ```sh
   docker-compose exec server alembic upgrade head
   ```
5. Visit http://localhost:3000/
6. To stop the containers, run
   ```shell
   docker-compose -f docker-compose.yml down -v
   ```
7. _Optional_: remove dangling images and volumes to reduce used storage
   ```sh
   docker image prune
   docker volume prune
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## Usage

### Running tests

TDD principle dictates
> Write test that fails and add just enough code to make the test pass.

The project uses this principle and extensibility of [`backend/tests/`](backend/tests) shows that.

To run the tests, use the command:
```sh
pytest -v backend/tests 
```

### Screenshots
Workflow of the service is explained in [About the Project](#about-the-project). The UI examples are below

<p float="left">
  <img src=phrosty-frontend/src/assets/img/LandingPage.png alt="Default" height="200" >
  <img src=phrosty-frontend/src/assets/img/LoginPage.png alt="Default" height="200" >
  <img src=phrosty-frontend/src/assets/img/ProfilePage.png alt="Default" height="200" >
</p>
<p float="left">
  <img src=phrosty-frontend/src/assets/img/SwaggerUIDocs.png alt="Default" width="600">
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Build schema using alembic migration file
- [x] Add authentication and registration
- [x] Add client-offer-evaluations logic
- [x] Create front-end views with state controlled by React Redux
- [x] Create navigation using React Router
- [x] Protect user-specific resources using hooks
- [x] Refactor login/registration to use hooks
- [ ] Allow sorting and filtering offers by price
- [ ] Add email notifications whenever offer status changes
- [ ] Add email notifications whenever cleaning status changes
- [ ] Create Behavior Driven Tests from client and cleaner points of view

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE.txt`](LICENSE.txt) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

Nurlat Bekdullayev - [@natuspati](https://twitter.com/natuspati) - natuspati@gmail.com

Project Link: [https://github.com/natuspati/phrosty](https://github.com/natuspati/phrosty)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Thanks to these resources that helped me to build the game.

* [ Jeff Astor's series on FastAPI and React](https://github.com/Jastor11/phresh-tutorial/tree/master).
* [Michael Herman: Developing and Testing an Asynchronous API with FastAPI and Pytest](https://testdriven.io/blog/fastapi-crud/)
* [Full Stack FastAPI and PostgreSQL - Base Project Generator](https://github.com/tiangolo/full-stack-fastapi-postgresql)
* [FastAPI Users](https://github.com/fastapi-users/fastapi-users)
* [SQL Bolt: interactive SQL queries](https://sqlbolt.com/lesson/introduction)
* [React Redux official docs](https://react-redux.js.org/tutorials/quick-start)
* [Othneil Drew: Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/natuspati/country-guess-game.svg?style=for-the-badge
[contributors-url]: https://github.com/natuspati/country-guess-game/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/natuspati/country-guess-game.svg?style=for-the-badge
[forks-url]: https://github.com/natuspati/country-guess-game/network/members
[stars-shield]: https://img.shields.io/github/stars/natuspati/country-guess-game.svg?style=for-the-badge
[stars-url]: https://github.com/natuspati/country-guess-game/stargazers
[issues-shield]: https://img.shields.io/github/issues/natuspati/country-guess-game.svg?style=for-the-badge
[issues-url]: https://github.com/natuspati/country-guess-game/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/nurlat/
[license-shield]: https://img.shields.io/github/license/natuspati/country-guess-game.svg?style=for-the-badge
[license-url]: https://github.com/natuspati/country-guess-game/blob/main/LICENSE.txt

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB

[React-url]: https://reactjs.org/

[fastapi.com]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white

[fastapi-url]: https://fastapi.tiangolo.com/

[ReactRouter.com]: https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white

[ReactRouter-url]: https://reactrouter.com/en/main

[ElasticUI.com]: https://img.shields.io/badge/ElasticUI-005571?style=for-the-badge&logo=elastic&logoColor=white

[ElasticUI-url]: https://eui.elastic.co/

[Docker.com]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white

[Docker-url]: https://www.docker.com/

[Redis.com]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white

[Redis-url]: https://redis.io/

[PostgreSQL.com]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white

[PostgreSQL-url]: https://www.postgresql.org/

[ReactRedux.com]: https://img.shields.io/badge/react_redux-764ABC?style=for-the-badge&logo=redux&logoColor=white

[ReactRedux-url]: https://react-redux.js.org/
