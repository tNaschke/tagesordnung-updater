[![de](https://img.shields.io/badge/language-german-green.svg)](https://github.com/tNaschke/tagesordnung-updater/blob/main/README.md)
[![en](https://img.shields.io/badge/language-english-blue.svg)](https://github.com/tNaschke/tagesordnung-updater/blob/main/README.en.md)


# Agenda Updater
The agenda updater publishes the agenda of the FSR Physics on its website. The agenda is also translated into English and published on the English website.


## Preparation
After the project has been downloaded, copies of all example files with the names `filename.example.extension` must be created as `filename.extension` and filled in.

To run the script, you need [Docker](https://docs.docker.com/get-docker/). As long as everything works, however, no knowledge of Docker should be necessary, just the commands below.


## Usage
To start the Tagesordnungs Updater, execute the following command in the project folder:
```bash
sudo docker compose up -d
```
The script is then started and runs in the background. The Docker container restarts itself in the event of problems, unless it has been terminated manually.

The agenda updater is terminated using the command
```bash
sudo docker compose down
```

If something has been changed in the program, the container must be rebuilt. To do this, terminate the agenda updater first and then start it as usual, but use the following command:
```bash
sudo docker compose up --build -d
```


## Configuration
### Website Template
The website is generated from the website template, which is automatically filled with the information. The template can be customized in the file `page.html` for the german website and `page.en.html` for the englisch website. Some variables can be used by writing them in curly brackets. The following variables are supported:
- `Datum`: The date of the session
- `TO`: The agenda of the meeting as a numbered list
