# GitHub setup

## Create the repository

1. Create a new empty GitHub repository named `visco-sensor`.
2. Do not initialize it with a README, license, or `.gitignore`; those files are included here.
3. From the extracted project directory, run:

```bash
git init
git add .
git commit -m "chore: initialize Visco-Sensor monorepo"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/visco-sensor.git
git push -u origin main
```

Replace `YOUR-USERNAME` with the account or organization that owns the repository.

## Add a collaborator

Open the repository's **Settings**, select **Collaborators**, and invite the other founder using their GitHub username or email address.

## Suggested repository description

> End-to-end IoT platform for ingesting, validating, and visualizing simulated wearable sensor telemetry.

## Suggested topics

`data-engineering`, `fastapi`, `nextjs`, `typescript`, `python`, `postgresql`, `mqtt`, `iot`, `health-tech`, `docker`
