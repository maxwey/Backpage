#!/bin/bash

# Set up the prod environment!
echo "Setting up the prod environment for Django!";

echo "Using $HOME as base dir";
cd $HOME;

if [ ! -d "Backpage" ]; then
  printf "Backpage root directory not present!!";
  exit -1;
fi

printf "Creating the secure random string used by the server...";
if [ ! -d "secure" ]; then
    mkdir secure;
    chmod 700 secure;
fi

touch secure/django_secret.txt;
openssl rand -base64 128 | tr -d "[:space:]" > secure/django_secret.txt;
chmod 400 secure/django_secret.txt;

printf "\e[1;32mDone\e[0m\n";


printf "Setting up static & media files..."
if [ ! -d "www" ]; then
    mkdir www;
    mkdir www/static-root;
    mkdir www/media-root;
    chmod -R 744 www;
fi

cd Backpage/backpage
python manage.py collectstatic
cd ../..

printf "\e[1;32mDone\e[0m\n";
