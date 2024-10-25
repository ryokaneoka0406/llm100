# Interviewer App with Realtime API

## Overview

This application is an AI-powered automated interview system. It collects personal information from users and creates a simple profile.

## Key Features

- User information collection (name, occupation, hobbies, favorite food, favorite movie)
- Display of collected information

## Tech Stack

- Next.js
- TypeScript
- OpenAI Realtime API

## Setup

1. Install dependencies
   ```
   npm install
   ```
2. Set up OpenAI API KEY in `index.tsx`

   ```typescript
   const client = new RealtimeClient({
     apiKey: "YOUR_OPENAI_API_KEY",
     dangerouslyAllowAPIKeyInBrowser: true,
   });
   ```

3. Start the application
   ```
   npm run dev
   ```

## How to Use

1. When you start the application, the AI interviewer will greet you and begin the interview.
2. As you answer the questions, your profile will be automatically created.
3. After the interview is complete, the collected information will be displayed on the screen.
