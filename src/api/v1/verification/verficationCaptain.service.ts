import TelegramService  from '../../../telegram/telegram.sevice';
import {escape} from 'html-escaper';

export class VerificationCaptainService {
  static async verifyCaptain(data) {
    const bot = TelegramService.getInstance();
    const chatId = process.env.CHAT_ID;
    await bot.telegram.sendMessage(chatId,`<b>Заявка на верифікацію старости</b>\n\n` +
      // `<b>Тег:<\b> ${captain.username}\n`+
      `<b>Ім'я:<\b> ${escape(data.firstName)}\n`+
      `<b>Прізвище:<\b> ${escape(data.middleName)}\n`+
      `<b>По батькові:<\b> ${escape(data.lastName)}\n`+
      `<b>Група:<\b> ${data.groupCode}\n`,
      {
        parse_mode: 'HTML',
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: 'Схвалити',
                callback_data: `approve_captain:${data.telegramId}`,
              },
            ],  
            [
              {
                text: 'Відмовити',
                callback_data: `deny_captain:${data.telegramId}`,
              },
            ]
          ],
        },
      }
    );
  }
}