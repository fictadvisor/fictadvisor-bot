import { Context } from 'telegraf';

export default () => {
  return async (ctx: Context) => {
    await ctx.reply('<b>Привіт від команди FICT Advisor!</b>\n\nАвторизація на сайті: /login\nЗворотній зв\'язок: @fict_robot\n', { parse_mode: 'HTML' });
  };
};
