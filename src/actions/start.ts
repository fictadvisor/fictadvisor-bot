import { Context } from 'telegraf';
import { v4 as uuidv4 } from 'uuid';
import {client} from "../api";
import NodeCache from "node-cache";

const cache = new NodeCache({stdTTL: 60*60});

export default () => async (ctx: Context) => {
  let id = cache.get(ctx.from.id);
  if (id == undefined) {
    id = uuidv4();
    cache.set(ctx.from.id, id);
  }
  const url = `${process.env.FRONT_BASE_URL}/oauth?token=${id}`;
  await client.post(`/auth/registerTelegram`, {
    token: id,
    telegramId: ctx.from.id,
  });

  await ctx.reply(`<b>Вітаємо вас у боті <a href="${process.env.FRONT_BASE_URL}">fictadvisor.com</a></b>\n` +
                  `Зворотній зв'язок: @fict_robot`, { parse_mode: 'HTML' });
  await ctx.reply(`<b>Для реєстрації перейдіть за почиланням</b>\n\n` +
                  `Якщо кнопка не працює, тицьни <a href="${url}">сюди</a>.`,
  { 
    parse_mode: 'HTML',
    disable_web_page_preview: true,
    reply_markup: {
      inline_keyboard: [
        [{text: 'Зареєструватись', url}],
      ],
    },
  });
};
