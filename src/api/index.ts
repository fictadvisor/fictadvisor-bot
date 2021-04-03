import axios from "axios";
import oauth from './oauth';

const client = axios.create({
    baseURL: process.env.API_BASE_URL,
    headers: { authorization: `Telegram ${process.env.BOT_TOKEN}` },
});

const api = {
    oauth: oauth(client),
};

export default api;
