# SETUP

## environment

```bash
touch .env
```

write your openai api key in .env file

## Install dependencies

### frontend

```bash
cd frontend
pnpm install
```

### backend

```bash
cd backend
pipenv install
pipevn shell
```

## Run

### frontend

```bash
cd frontend
pnpm run dev
```

### backend

```bash
cd backend
uvicorn main:app --reload
```
