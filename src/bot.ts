import TelegramService  from './telegram/telegram.sevice';
import start from './actions/start';
import debug from './actions/debug';
import * as process from 'process';
import {ApproveCaptain} from "./actions/approve.captain";
import {DenyCaptain} from "./actions/deny.captain";
import {ApproveStudent} from "./actions/approve.student";
import {DenyStudent} from "./actions/deny.student";
import {ApproveSuperhero} from "./actions/approve.superhero";
import {DenySuperhero} from "./actions/deny.superhero";
import {ApproveResponse} from "./actions/approve.response";
import {DenyResponse} from "./actions/deny.response";

const bot = TelegramService.getInstance(process.env.BOT_TOKEN);

bot.start(start());
bot.command('/debug', debug());

bot.action(/^1:.+:approve:\w+$/, async (ctx) => {
  const handler = new ApproveCaptain(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(/^1:.+:deny:\w+$/, async (ctx) => {
  const handler = new DenyCaptain(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(/^2:.+:approve:\w+$/, async (ctx) => {
  const handler = new ApproveStudent(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(/^2:.+:deny:\w+$/, async (ctx) => {
  const handler = new DenyStudent(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(/^3:.+:approve:\w+$/, async (ctx) => {
  const handler = new ApproveSuperhero(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(/^3:.+:deny:\w+$/, async (ctx) => {
  const handler = new DenySuperhero(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(/^response:.+:approve$/, async (ctx) => {
  const handler = new ApproveResponse(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(/^response:.+:deny$/, async (ctx) => {
  const handler = new DenyResponse(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

export default bot;
