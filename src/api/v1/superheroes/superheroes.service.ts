import TelegramService  from '../../../telegram/telegram.sevice';

export class SuperheroesService {
    static async broadcastPending(data) {
        const bot = TelegramService.getInstance();
        const chatId = process.env.CHAT_ID;
        await bot.telegram.sendMessage(chatId,`<b>Заявка на супергероя</b>\n\n` +
            `<b>Від:</b> ${data.first_name} (${data.username ? `@${data.username}, ` : ''}${data.id})\n\n` +
            `<b>Ім'я:</b> ${escape(data.name)}\n` +
            `<b>Юзернейм:</b> @${escape(data.username)}\n` +
            `<b>Курс:</b> ${data.year}\n` +
            `<b>Гуртожиток:</b> ${data.dorm ? 'так' : 'ні'}`,
            {
                parse_mode: 'HTML',
                reply_markup: {
                    inline_keyboard: [
                        [
                            {
                                text: 'Схвалити',
                                callback_data: `approve_superhero:${data.id}:${data.telegram_id}`,
                            },
                        ],
                        [
                            {
                                text: 'Відмовити',
                                callback_data: `deny_superhero:${data.id}:${data.telegram_id}`,
                            },
                        ],
                    ],
                },
            });
    }
}