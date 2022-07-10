import { Context } from 'telegraf'

export default () => {
  return async (ctx: Context) => {
    await ctx.deleteMessage(ctx.callbackQuery.message.message_id)
    await ctx.answerCbQuery()
  }
}
