import axios from "axios";
import { RequestHandler } from "express";

export default (): RequestHandler => async (req, res) => {
    const { url } = req.query;

    if (url == null || url == '') {
        res.status(400).send();
        return;
    }

    try {
        const { data } = await axios.get(`https://api.telegram.org/file/bot${process.env.BOT_TOKEN}/${url}`, { responseType: 'stream'});
        data.pipe(res);
    } catch (e) {
        res.status(e.response?.status ?? 404).send(e.response?.message ?? e.message);
    }
};
