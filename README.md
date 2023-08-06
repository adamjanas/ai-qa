## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Launch](#launch)

## General info
It's an ai-qa repo. As the name suggests, project showcases usage of q&a chatbot based on given content.

Simply u can load some urls and ask some questions.


## Technologies
Project is created with:
* [fastapi](https://fastapi.tiangolo.com/)
* [poetry](https://python-poetry.org)
* [langchain](https://docs.langchain.com/docs/)
* [openai](https://pypi.org/project/openai/)
* [qdrant as vector search engine](https://qdrant.tech/)
* [docker](https://www.docker.com/)

## Launch
[poetry](https://python-poetry.org) is a package-manager tool of the project.

Create appropriate directory for the project and clone repository to your local machine

```bash
$ cd <your_desired_location>
$ git clone <repo_address>
```

Generate virtual environment and install all needed dependencies

```bash
$ poetry install
```

If you need help or more info about poetry, run:

```bash
$ poetry --help
```