Procfile is for pushing to heroku. Heroku steps

installing heroku on OSx

```
brew install heroku
```

Make sure you are logged in

```
heroku login
```

Then these commands will get you up and running

```
heroku create <subdomain-name>
git push heroku master # for branch pushes: git push heroku testbranch:main
```

you can delete your heroku git

```
git remote -v
git remote rm heroku
```

```
heroku git:remote -a thawing-inlet-61413
```

```
git remote rename heroku heroku-staging
```

#### this can be used to differentiate between the prod and staging

some other useful heroku commands

```
heroku config:set ENVIRON_NAME=environ_value
heroku apps:rename newname
```
