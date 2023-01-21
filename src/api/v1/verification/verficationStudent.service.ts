import TelegramService  from '../../../telegram/telegram.sevice';
import {escape} from 'html-escaper';

export class VerificationStudentService {
    static async verifyStudent(data) {
        const bot = TelegramService.getInstance();
        await bot.telegram.sendMessage(data.captain.telegramId,`<b>Заявка на верифікацію студента</b>\n\n` +
            // `<b>Тег:<\b> ${userUsername}\n`+
            `<b>Ім'я:<\b> ${escape(data.user.firstName)}\n`+
            `<b>Прізвище:<\b> ${escape(data.user.middleName)}\n`+
            `<b>По батькові:<\b> ${escape(data.user.lastName)}\n`+
            `<b>Група:<\b> ${data.user.groupCode}\n`,
            {
                parse_mode: 'HTML',
                reply_markup: {
                    inline_keyboard: [
                        [
                            {
                                text: 'Схвалити',
                                callback_data: `approve_student:${data.user.telegramId}`,
                            },
                        ],
                        [
                            {
                                text: 'Відмовити',
                                callback_data: `deny_student:${data.user.telegramId}`,
                            },
                        ],
                    ],
                },
            });
    }
}