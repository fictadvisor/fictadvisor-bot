import { Telegraf } from 'telegraf';
import login from './actions/login';
import start from './actions/start';
import cancelLogin from './actions/cancelLogin';
import debug from './actions/debug';
import Action from './actions/action.surrounder';
import { ActionsFactory } from './actions/actions.factory';

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.hears(/^(\/start login|\/login)$/g, login());
bot.start(start());
bot.command('/debug', debug());

const callbackQueries = [
  { match: data => data === 'cancel_login', handler: cancelLogin() }
];

bot.on('callback_query', async ctx => {
  const data = (ctx.callbackQuery as any).data as string;
  const handler: Action = ActionsFactory.create(data, ctx);

  if (handler !== null) {
    try {
      await handler.execute();
    } catch (e) {
      handler.catch(e);
    }
  } else {
    for (const { match, handler } of callbackQueries) {
      if (!match(data)) continue;
      return handler(ctx);
    }
  }
});

export default bot;
