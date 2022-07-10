import { Context } from 'telegraf'

export default () => {
  return async (ctx: Context) => {
    await ctx.reply(`User ID: <pre>${ctx.from.id}</pre>\nChat ID: <pre>${ctx.chat.id}</pre>`, { parse_mode: 'HTML' })
  }
}
