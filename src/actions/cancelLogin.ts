import { Context } from 'telegraf';

export default () => async (ctx: Context) => {
  await ctx.deleteMessage(ctx.callbackQuery.message.message_id);
  await ctx.answerCbQuery();
};
