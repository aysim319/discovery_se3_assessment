# Discovery SE3 take home assessment

## Specification
Please set up a Python script that meets the following requirements:

Use the NASA API (https://api.nasa.gov/) to retrieve the Astronomy Picture of the Day

Based on the title (or description) of the photo, retrieve some additional details about the photo. You can use any source(s) you want but we’ve included a few examples you might find useful:

 - Wikipedia (https://www.mediawiki.org/wiki/API:Opensearch)

 - Google results

 - LLM

Return a dictionary with the photo source, info about the photo from NASA, and the additional information you retrieved in step 2.

Provide some unit tests - unittest is our preference but pytest is ok.

Please try not to spend more than 2 hours on this project. You can send this as a github repo or a zipped directory including a README on how to run the script if necessary.

If you’ve had to make any assumptions in order to build your script, list them in the README. 



## Setup

If the code is grabbed from the repo
   1. Generate API key from https://api.nasa.gov/ by registering with name and email
   2. In the `src` directory, create an empty `.env` file and copy-paste the api key gotten from the email
      ```
      API_KEY=xxxxx
      APOD_API=https://api.nasa.gov/planetary/apod?api_key=${API_KEY}
      WIKI_API=https://en.wikipedia.org/w/api.php
      ```
If running directly from a tarball, then skip steps 1 and 2.

   3. In the project directory, create a virtual env with the command ```python3 -m venv venv```
   4. From the project root directory, activate the virtual environment with the command ```source venv/bin/activate```
   5. install the necessary packages with the command ```pip install -r requirements.txt```
      - update pip with command ```pip install --upgrade pip``` if needed

After the setup the directory should look something like this
```
.
├── README.md
├── requirements.txt
├── venv
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── .env
│   └── utils
│       ├── __init__.py
│       └── fetch_data.py
└── test
    ├── __init__.py
    ├── data
    │   ├── 2023-04-01-apod-wiki-results.json
    │   ├── 2023-04-01-apod.json
    │   └── 2023-04-01-wiki-extlinks.json
    └── test_fetch_data.py

```


## Usage

after completing setup run command ```cd src && python3 main.py```

- with no command line options it will run and grab current date of execution's APOD and save the output as a json in the src/out directory with the format ```YYYY-MM-DD-apod-data.json```
