---
title: Deploying DATA act Pilot app to Cloud Foundry
---
These instructions are for the 18F team. They explain how to deploy the DATA Act pilot to Cloud Foundry. The following steps are best done through the command line. 

## Set up Cloud Foundry on your computer
Follow [our documentation](https://docs.18f.gov/getting-started/setup/), using the  information outlined below.

1. Set up your account by [creating an issue in the DevOps issue tracker](https://github.com/18F/DevOps/issues/new). 
2. Log in with `cf login`.
3. Connect to the 18F API with `cf api https://api.18f.gov`.
4. Enter your username (GSA email) and password.
5. A prompt will ask you to choose an org. Select `data-act`.
6. Another prompt will ask you to choose a space. Select `pilot-dev`.
7. Complete steps 5 and 6 using the command `cf target -o data-act -s pilot-dev`.
8. Make sure you're in the `app/` folder of the data-act repository.
9. Build the site using the command `cf push data-act-pilot-v2 -d 18f.gov`.

## Update authorization credentials: 
1. Log in.
2. Set the username using the command `cf set-env data-act-pilot-v2  WEB_USERNAME '<username>'`.
3. Set the password using the command  `cf set-env data-act-pilot-v2  WEB_PASSWORD '<password>'`.
4. Check if those credentials saved with the command `cf restage data-act-pilot`.



