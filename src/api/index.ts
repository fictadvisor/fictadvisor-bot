import axios from "axios";
import oauth from './oauth';
import reviews from "./reviews";

const client = axios.create({
    baseURL: process.env.API_BASE_URL,
    headers: { authorization: `Telegram ${process.env.BOT_TOKEN}` },
});

const api = {
    oauth: oauth(client),
    reviews: reviews(client),
};

export default api;
