import { Telegraf } from "telegraf";
import login from './actions/login';
import start from "./actions/start";
import cancelLogin from "./actions/cancelLogin";
import debug from "./actions/debug";
import approveReview from "./actions/approveReview";
import denyReview from "./actions/denyReview";

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.hears(/^(\/start login|\/login)$/g, login());
bot.start(start());
bot.command('/debug', debug());

const callbackQueries = [
    { match: (data) => data === 'cancel_login', handler: cancelLogin() },
    { match: (data) => /^approve_review:.+/.test(data), handler: approveReview() },
    { match: (data) => /^deny_review:.+/.test(data), handler: denyReview() },
];

bot.on('callback_query', (ctx) => {
    const data = (ctx.callbackQuery as any).data as string;

    for (let { match, handler } of callbackQueries) {
        if (match(data)) {
            return handler(ctx);
        }
    }
});

export default bot;
