import { Telegraf } from "telegraf";
import login from './actions/login';
import start from "./actions/start";
import cancelLogin from "./actions/cancelLogin";
import debug from "./actions/debug";
import approveReview from "./actions/approveReview";
import denyReview from "./actions/denyReview";
import approveSuperhero from "./actions/approveSuperhero";
import denySuperhero from "./actions/denySuperhero";
import approveTeacher from './actions/approveTeacher';
import denyTeacher from './actions/denyTeacher';
import approveCourse from './actions/approveCourse';
import denyCourse from './actions/denyCourse';

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.hears(/^(\/start login|\/login)$/g, login());
bot.start(start());
bot.command('/debug', debug());

const callbackQueries = [
    { match: (data) => data === 'cancel_login', handler: cancelLogin() },
    { match: (data) => /^approve_review:.+/.test(data), handler: approveReview() },
    { match: (data) => /^deny_review:.+/.test(data), handler: denyReview() },
    { match: (data) => /^approve_superhero:.+/.test(data), handler: approveSuperhero() },
    { match: (data) => /^deny_superhero:.+/.test(data), handler: denySuperhero() },
    { match: (data) => /^approve_teacher:.+/.test(data), handler: approveTeacher() },
    { match: (data) => /^deny_teacher:.+/.test(data), handler: denyTeacher() },
    { match: (data) => /^approve_course:.+/.test(data), handler: approveCourse() },
    { match: (data) => /^deny_course:.+/.test(data), handler: denyCourse() },
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
