import TelegramService  from '../../../telegram/telegram.sevice';

export class ReviewsService {
    static async broadcastPending(data) {
        const bot = TelegramService.getInstance();
        const chatId = process.env.CHAT_ID;
        await bot.telegram.sendMessage(chatId,`<b>Відгук на <a href="${process.env.FRONT_BASE_URL}/courses/${data.course.link}">${data.course.link}</a>\n` +
            `Автор: ${data.user.first_name} (${data.user.id})\nОцінка: ${data.review.rating}</b>\n\n` +
            `<pre>${escape(data.review.content)}</pre>`,
            {
                parse_mode: 'HTML',
                reply_markup: {
                    inline_keyboard: [
                        [
                            {
                                text: 'Схвалити',
                                callback_data: `approve_review:${data.user.id}:${data.user.telegram_id}`,
                            },
                        ],
                        [
                            {
                                text: 'Відмовити',
                                callback_data: `deny_review:${data.user.id}:${data.user.telegram_id}`,
                            },
                        ],
                    ],
                },
            });
    }
}