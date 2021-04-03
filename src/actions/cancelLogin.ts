import { Context } from "telegraf";

export const CANCEL_LOGIN_QUERY = 'cancel_login';

export default () => {
    return async (ctx: Context) => {
        await ctx.deleteMessage(ctx.callbackQuery.message.message_id);
        await ctx.answerCbQuery();
    };
};
