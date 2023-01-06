import TelegramService  from '../../../telegram/telegram.sevice';

export class TeachersService {
    static async broadcastPending(data) {
        const bot = TelegramService.getInstance();
        const chatId = process.env.CHAT_ID;
        await bot.telegram.sendMessage(chatId,`<b>Заявка на додавання викладача</b>\n\n` +
            `<b><a href="${process.env.FRONT_BASE_URL}/teachers/${data.teacher.link}">${data.teacher.fullname}</a></b> (${data.teacher.id})\n` +
            `<b>Автор</b>: ${data.user.first_name}`,
            {
                parse_mode: 'HTML',
                reply_markup: {
                    inline_keyboard: [
                        [
                            {
                                text: 'Схвалити',
                                callback_data: `approve_teacher:${data.teacher.id}:${data.user.telegramId}`,
                            },
                        ],
                        [
                            {
                                text: 'Відмовити',
                                callback_data: `deny_teacher:${data.teacher.id}:${data.user.telegramId}`,
                            },
                        ],
                    ],
                },
            });
    }
}