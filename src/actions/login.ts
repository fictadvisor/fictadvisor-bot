import { CANCEL_LOGIN_QUERY } from "./cancelLogin";
import { Context } from "telegraf";
import api from "../api";

export default () => {
    return async (ctx: Context) => {
        const { from } = ctx;

        try {
            const { data } = await api.oauth.telegram({ 
                telegram_id: from.id,
                first_name: from.first_name,
                last_name: from.last_name,
                username: from.username,
            });
        
            const url = `${process.env.BASE_URL}/oauth?access_token=${data.access_token}&refresh_token=${data.refresh_token}`;

            await ctx.reply(`<b>Авторизація на сайті fictadvisor.com</b>\n\nМы не передаємо і не будемо ніколи передавати твої дані.\nВони лише використовуються в межах авторизації та ідентифікації нашої системи.\n\n<b>Якщо кнопка не працює, тицьни <a href="${url}">сюди</a>.</b>`, {
                parse_mode: 'HTML',
                reply_markup: {
                    inline_keyboard: [
                        [{ text: 'Авторизуватись', url }],
                        [{ text: 'Відмінити', callback_data: CANCEL_LOGIN_QUERY }],
                    ],
                },
            });
        } catch (e) {
            console.error(`Authorization failed (${from.first_name}, ${from.id}): ${e}`);

            await ctx.reply('<b>На жаль, наразі наші сервіси недоступні. Спробуй авторизуватись через декілька хвилин.</b>\n\n/login', { parse_mode: 'HTML' });
        }
    };
};
