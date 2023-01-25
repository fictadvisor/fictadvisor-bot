import TelegramService  from '../../../telegram/telegram.sevice';
import {escape} from 'html-escaper';
import {SuperheroDto} from "./dto/superhero.dto";

export class SuperheroesService {
  static async broadcastPending(data: SuperheroDto) {
    const bot = TelegramService.getInstance();
    const chatId = process.env.CHAT_ID;
    await bot.telegram.sendMessage(chatId, `<b>Заявка на супергероя</b>\n\n` +
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

  static async broadcastApprovedSuperhero(id) {
    const bot = TelegramService.getInstance();
    await bot.telegram.sendMessage(
      id,
      `<b>Вітаємо тебе, ти — супергерой!</b>`,
      {
        parse_mode: 'HTML',
      }
    );
  }

  static async broadcastDeclinedSuperhero(id) {
    const bot = TelegramService.getInstance();
    await bot.telegram.sendMessage(
      id,
      `<b>На жаль, твій запит на супергероя було відхилено.</b>\n\n` +
            `Якщо в тебе є питання, звертайся до нас через бота зворотнього зв'язку: @fict_robot`,
      {
        parse_mode: 'HTML',
      }
    );
  }
}