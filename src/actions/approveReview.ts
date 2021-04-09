import api from "../api";
import { Context } from "telegraf";
import { AxiosError } from 'axios';

export default () => {
    return async (ctx: Context) => {
        const id = (ctx.callbackQuery as any).data.split(':')[1];
        const { message, inline_message_id, from } = ctx.callbackQuery;

        try {
            await api.reviews.update(id, { state: 'approved' });

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
            const axiosError = e as AxiosError;

            if (axiosError.isAxiosError) {
                if (axiosError.response?.status === 404) {
                    await ctx.telegram.editMessageText(
                        message.chat.id, 
                        message.message_id,
                        inline_message_id,
                        `<b>Відгук ${id} вже було видалено.</b>`,
                        {
                            parse_mode: 'HTML',
                        }
                    );

                    return;
                }
            }

            console.error(e);
            
            await ctx.reply(e.toString(), { reply_to_message_id: message.message_id });
        }
    };
};
