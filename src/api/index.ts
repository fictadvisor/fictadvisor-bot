import axios from 'axios';

export const client = axios.create({
  baseURL: process.env.API_BASE_URL,
  headers: { authorization: `Telegram ${process.env.BOT_TOKEN}` },
});
