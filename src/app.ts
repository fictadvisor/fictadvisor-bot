import { Telegraf } from "telegraf";
import login from './actions/login';
import start from "./actions/start";
import cancelLogin from "./actions/cancelLogin";

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.hears(/^(\/start login|\/login)$/g, login());
bot.start(start());
bot.on('callback_query', cancelLogin());

export default bot;
