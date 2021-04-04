import api from "../api";
import { Context } from "telegraf";

export default () => {
    return async (ctx: Context) => {
        try {
            const id = (ctx.callbackQuery as any).data.split(':')[1];
            await api.reviews.update(id, { state: 'approved' });

            const { message, inline_message_id, from } = ctx.callbackQuery;

            await ctx.telegram.editMessageText(
                message.chat.id, 
                message.message_id,
                inline_message_id,
                `<b>Відгук ${id} схвалено.</b>\n\n` +
                `<b>Ким:</b> <a href="tg://user?id=${from.id}">${from.username ? `@${from.username}` : from.first_name}</a>\n` +
                `<b>Коли:</b> ${new Date().toISOString()}`,
                {
                    parse_mode: 'HTML',
                    reply_markup: {
                        inline_keyboard: [
                            [{ text: 'Скасувати та видалити', callback_data: `deny_review:${id}` }]
                        ],
                    },
                }
            );
        } catch (e) {
            console.error(e);
            await ctx.reply(`Щось пішло не так: ${e}`);
        }
    };
};
