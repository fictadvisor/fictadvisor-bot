import TelegramService from '../../../telegram/telegram.sevice';
import {escape} from 'html-escaper';
import {CaptainDto} from "./dto/captain.dto";

export class CaptainsService {
  static async broadcastPending(data: CaptainDto) {
    const bot = TelegramService.getInstance();
    const chatId = process.env.CHAT_ID;
    await bot.telegram.sendMessage(chatId, `<b>Заявка на старосту</b>\n\n` +
            `<b>Від:</b> ${data.first_name} (${data.username ? `@${data.username}, ` : ''}${data.id})\n\n` +
            `<b>Ім'я:</b> ${escape(data.name)}\n` +
            `<b>Юзернейм:</b> @${escape(data.username)}\n` +
            `<b>Курс:</b> ${data.year}\n` +
            `<b>Група:</b> ${escape(data.group_code)}`,
    {
      parse_mode: 'HTML',
      reply_markup: {
        inline_keyboard: [
          [
            {
              text: 'Схвалити',
              callback_data: `approve_captain:${data.id}:${data.telegram_id}`,
            },
          ],
          [
            {
              text: 'Відмовити',
              callback_data: `deny_captain:${data.id}:${data.telegram_id}`,
            },
          ],
        ],
      },
    });
  }

  static async broadcastApprovedCaptain(id) {
    const bot = TelegramService.getInstance();
    await bot.telegram.sendMessage(
      id,
      `<b>Вітаємо тебе, ти — староста!</b>`,
      {
        parse_mode: 'HTML',
      }
    );
  }

  static async broadcastDeclinedCaptain(id) {
    const bot = TelegramService.getInstance();
    await bot.telegram.sendMessage(
      id,
      `<b>На жаль, твій запит на старосту було відхилено.</b>\n\n` +
            `Якщо в тебе є питання, звертайся до нас через бота зворотнього зв'язку: @fict_robot`,
      {
        parse_mode: 'HTML',
      }
    );
  }
}