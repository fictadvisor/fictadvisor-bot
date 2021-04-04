import { Telegraf } from "telegraf";
import login from './actions/login';
import start from "./actions/start";
import cancelLogin from "./actions/cancelLogin";
import debug from "./actions/debug";

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.hears(/^(\/start login|\/login)$/g, login());
bot.start(start());
bot.command('/debug', debug());
bot.on('callback_query', cancelLogin());

export default bot;
