import TelegramService  from './telegram/telegram.sevice';
import start from './actions/start';
import debug from './actions/debug';
import * as process from 'process';
import {captainData} from "./callbacks/captain";
import {ApproveCaptain} from "./actions/approve.captain";
import {DenyCaptain} from "./actions/deny.captain";
import {studentData} from "./callbacks/student";
import {ApproveStudent} from "./actions/approve.student";
import {DenyStudent} from "./actions/deny.student";
import {superheroData} from "./callbacks/superhero";
import {ApproveSuperhero} from "./actions/approve.superhero";
import {DenySuperhero} from "./actions/deny.superhero";

const bot = TelegramService.getInstance(process.env.BOT_TOKEN);

bot.start(start());
bot.command('/debug', debug());

bot.action(captainData.filter({
  method:"approve",
}), async (ctx) => {
  const handler = new ApproveCaptain(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(captainData.filter({
  method:"deny",
}), async (ctx) => {
  const handler = new DenyCaptain(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(studentData.filter({
  method:"approve",
}), async (ctx) => {
  const handler = new ApproveStudent(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(studentData.filter({
  method:"deny",
}), async (ctx) => {
  const handler = new DenyStudent(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(superheroData.filter({
  method:"approve",
}), async (ctx) => {
  const handler = new ApproveSuperhero(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

bot.action(superheroData.filter({
  method:"deny",
}), async (ctx) => {
  const handler = new DenySuperhero(ctx);
  try {
    await handler.execute();
  } catch (e) {
    handler.catch(e);
  }
});

export default bot;
