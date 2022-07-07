import { Telegraf } from "telegraf";
import login from './actions/login';
import start from "./actions/start";
import cancelLogin from "./actions/cancelLogin";
import debug from "./actions/debug";
import Action from "./actions/action.surrounder";
import {ApproveReview} from "./actions/approve.review";
import {ApproveCourse} from "./actions/approve.course";
import {ApproveSuperhero} from "./actions/approve.superhero";
import {ApproveTeacher} from "./actions/approve.teacher";
import {ApproveSubject} from "./actions/approve.subject";
import {ApproveTeachersContact} from "./actions/approve.teachers.contact";
import {DenySuperhero} from "./actions/deny.superhero";
import {DenyTeacher} from "./actions/deny.teacher";
import {DenyCourse} from "./actions/deny.course";
import {DenySubject} from "./actions/deny.subject";
import {DenyTeachersContact} from "./actions/deny.teachers.contact";
import {DenyReview} from "./actions/deny.review";

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.hears(/^(\/start login|\/login)$/g, login());
bot.start(start());
bot.command('/debug', debug());

const callbackQueries = [
    { match: (data) => data === 'cancel_login', handler: cancelLogin() },
    { match: (data) => /^approve_review:.+/.test(data), handler: new ApproveReview() },
    { match: (data) => /^deny_review:.+/.test(data), handler: new DenyReview() },
    { match: (data) => /^approve_superhero:.+/.test(data), handler: new ApproveSuperhero() },
    { match: (data) => /^deny_superhero:.+/.test(data), handler: new DenySuperhero() },
    { match: (data) => /^approve_teacher:.+/.test(data), handler: new ApproveTeacher() },
    { match: (data) => /^deny_teacher:.+/.test(data), handler: new DenyTeacher() },
    { match: (data) => /^approve_course:.+/.test(data), handler: new ApproveCourse() },
    { match: (data) => /^deny_course:.+/.test(data), handler: new DenyCourse() },
    { match: (data) => /^approve_subject:.+/.test(data), handler: new ApproveSubject() },
    { match: (data) => /^deny_subject:.+/.test(data), handler: new DenySubject() },
    { match: (data) => /^approve_contact:.+/.test(data), handler: new ApproveTeachersContact() },
    { match: (data) => /^deny_contact:.+/.test(data), handler: new DenyTeachersContact() },
];

bot.on('callback_query', async (ctx) => {
    const data = (ctx.callbackQuery as any).data as string;

    for (let { match, handler } of callbackQueries) {
        if (!match(data)) continue;
        if (handler instanceof Action) {
            handler.ctx = ctx;
            try {
                await handler.execute();
            } catch (e) {
                handler.catch(e);
            }
        } else {
            return handler(ctx);
        }
    }
});

export default bot;
