import { Context } from 'telegraf';

export default () => async (ctx: Context) => {
  const url = `${process.env.FRONT_BASE_URL}/oauth`;

  await ctx.reply(`<b>Вітаємо вас у боті <a href="https://fictadvisor.com">fictadvisor.com</a></b>\n` +
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
