# Asset Tracker
Asset tracker is a tool used to track and manage the components in a base unit. There are three main types of component: base unit, camera, other item. Each type can have notes and maintenance tasks associated with it. There are also reports that can be generated concerning the maintnenance status of each item type.

## Technology Stack
![Archiutecture](/images/prototype.drawio.png)

### Frontend
* Vuteify
* Vue
* Javascript

### Backend
* Python
* FastAPI

### Database
* Postgres

## Local Testing
You can use docker-compose to build a set of local containers to test locally prior to pusing your changes to the production branch. This process will build trhe following containers:

1. db - postgres database 
2. inventory-backend - The backend fastapi server written in python.
3. inventory-frontend - The frontend vuetify/vue/javascript server.

To run the containers, from the django root directory:

```
# To build and start the 3 containers.
docker compose build
docker compose up

# To run the containers as daemons.
docker compose up -d

# To stop the containers.
docker compose stop
```
Not that using docker compose down will wipe away any data in the db, so I avoid it.

## Remote deploy
Build the frontend and push it to gcr.io. This command is for a mac.
```
cd frontend/inventory
docker buildx build --no-cache --platform linux/amd64,linux/arm64 --output "type=image,push=true" -t australia-southeast1-docker.pkg.dev/mystic-subject-483013-s9/asset-tracker/frontend:latest .
```

Build the backend and push it to gcr.io. This command is for a mac.
```
cd backend
docker buildx build --no-cache --platform linux/amd64,linux/arm64 --output "type=image,push=true" -t australia-southeast1-docker.pkg.dev/mystic-subject-483013-s9/asset-tracker/backend:latest .
```

Go to the google console then go to Cloud Run. From Services, select the resource to build (either frontend or backend). Select "Edit & deploy new revision". Pick the new "Container Image URL" and hit "Deploy".
