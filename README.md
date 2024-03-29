<p align="center">
  <a href="https://github.com/fictadvisor/fictadvisor-bot">
    <img src="https://i.imgur.com/ChzUSaU.png" alt="Logo" width="80px">
  </a>

  <h3 align="center">BOT</h3>

  <p align="center">
    Bot application for <a href="https://fictadvisor.com">fictadvisor.com</a>
    <br />
    <a href="https://github.com/fictadvisor/fictadvisor-bot/wiki"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://fictadvisor.com">View the Website</a>
    ·
    <a href="https://github.com/fictadvisor/fictadvisor-bot/issues">Report a Bug</a>
    ·
    <a href="https://github.com/fictadvisor/fictadvisor-bot/issues">Request a Feature</a>
  </p>
</p>

<details open="open">
  <summary>Table of contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

## About the project
This application provides a Telegram Bot application for FICT Advisor.

### Built with

* [Aiogram](https://aiogram.dev/)
* [FastApi](https://fastapi.tiangolo.com/)

## Getting started

To get a local copy up and running follow these steps.

### Prerequisites

* Python
* pip
* Poetry (pip install poetry)

### Installation

**ALL FOLLOWED COMMANDS MUST BE USED IN PROJECT DIRECTORY**

1. Clone the repository
   ```sh
   git clone https://github.com/fictadvisor/fictadvisor-bot.git
   ```
2. Install python packages
   ```sh
   poetry install
   ```
3. PM Team-Lead to receive .env configuration.

## Usage

To start the application:

  * If you use PyCharm:

    ```sh
    uvicorn app.main:app --reload
    ```

  * If you use VS Code:

    1. Activate poetry shell

    ```sh
    poetry shell
    ```

    2. Start the application:

    ```sh
    uvicorn app.main:app --reload
    ```

## Roadmap

See the [open issues](https://github.com/fictadvisor/fictadvisor-bot/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Added an amazing feature'`)
4. Push the branch (`git push -u origin feature/amazing-feature`)
5. Open a pull request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Feedback - [https://t.me/fict_robot](https://t.me/fict_robot)
Project - [https://github.com/fictadvisor](https://github.com/fictadvisor)

## Acknowledgements
* [Aiogram](https://aiogram.dev/)
* [Pydantic](https://docs.pydantic.dev/)
* [FastApi](https://fastapi.tiangolo.com/)
