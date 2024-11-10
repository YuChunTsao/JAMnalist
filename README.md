# JAMnalist

A Smart Semi-automatic Activity Notifier for HackMD

## Development

### Setup Python Environment

```bash
python -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Create API Token and Webhook URL

In this project, we use HackMD API and Discord Webhook URL to create a bot that notifies users about their activities on HackMD.

To use the bot, you need to create an API token on HackMD and a Webhook URL on Discord.

If use want to run the script locally, you need to create a `.env` file in the root directory with the following content:

```text
HACKMD_API_KEY="xxx"
DISCORD_WEBHOOK_URL="xxx"
```

> You can copy the `.env.example` file and rename it to `.env` to set the environment variables.

#### HackMD API Token

- Go to [HackMD](https://hackmd.io) and login
- Click on `Settings` -> `API` -> `Create API Token`
- Type a name for the token and click on `Create`
- Copy the token and save it in the `.env` file

#### Discord Webhook URL

- Go to Server Settings -> Integrations -> Webhooks -> New Webhook
- Copy the Webhook URL and save it in the `.env` file

## Usage

You can run the script using the following command:

```bash
python checkHackmdUpdates.py
```

> Note: You need to set the `HACKMD_API_KEY` and `DISCORD_WEBHOOK_URL` environment variables before running the script.
> It will send a message to your Discord channel with the latest updates on your HackMD documents.

## Deployment

The script will be deployed using GitHub Actions. You need to set the `HACKMD_API_KEY`, `DISCORD_WEBHOOK_URL`, and `PAT`(Personal Access Token) secrets in the repository settings.

- `Repository` -> `Settings` -> `Secrets and variables` -> `Actions`
- Click on `New repository secret`
- Create a secret with the name `HACKMD_API_KEY` and paste the API token
- Create a secret with the name `DISCORD_WEBHOOK_URL` and paste the Webhook URL

### PAT (Personal Access Token)

- Go to [GitHub](https://github.com) and login
- Click on `Settings` -> `Developer settings` -> `Personal access tokens` -> `Generate new token`
- Copy the token and save it in the repository secrets (`PAT`)
