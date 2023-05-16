to run locally use command:
  uvicorn main:app --reload

google cloud deploy:
  command line inside root directory:
    gcloud app deploy --project packerusermanagement -v {version number, integer value}
  
  reference:
    https://cloud.google.com/sdk/gcloud/reference/app/deploy

  assumes Google Cloud SDK installation:
    https://cloud.google.com/sdk/docs/quickstart


  create requirements:
    pip3 freeze > requirements.txt

local hosting:
  Without local installation of PostgreSQL:
    create "env_variables.yaml" file that contains all secrets for connecting to cloud database and email (gmail) service.

  Wit local installation of PostgreSQL:
    install PostgreSQL
    create database
    create "env_variables.yaml" file that contains all secrets for connecting to local database and email (gmail) service.
