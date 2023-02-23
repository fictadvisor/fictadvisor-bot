import TelegramService  from '../../../telegram/telegram.sevice';
import {SuperheroDTO} from "./dto/superhero.dto";
import {superheroData} from "../../../callbacks/superhero";
import {Markup} from "telegraf";

export class SuperheroesService {
  static async broadcastPending(data: SuperheroDTO) {
    const bot = TelegramService.getInstance();
    const user = (data.telegramId ? (await bot.telegram.getChat(data.telegramId)) as any : undefined);
    const chatId = process.env.CHAT_ID;
    await bot.telegram.sendMessage(chatId, `<b>Заявка на старосту</b>\n\n` +
            `<b>Від:</b> ${data.lastName} ${data.firstName} ${data.middleName ? `${data.middleName}` : ``}\n` +
            (user ? `<b>Юзернейм:</b> <a href="tg://user?id=${user.id}">${user.username ? `@${user.username}` : `${user.first_name}`}</a>\n` : ``) +
            `<b>Група:</b> ${data.groupCode}\n` +
            `<b>Гуртожиток:</b> ${data.dorm ? 'так' : 'ні'}`,
    {
      parse_mode: 'HTML',
      ...Markup.inlineKeyboard([
        Markup.button.callback(
          "Схвалити",
          superheroData.pack({
            method: "approve",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
        Markup.button.callback(
          "Відмовити",
          superheroData.pack({
            method: "deny",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
      ]),
    });
  }

  static async broadcastApprovedSuperhero(id) {
    if (id != 'undefined') {
      const bot = TelegramService.getInstance();
      await bot.telegram.sendMessage(
        id,
        `<b>Вітаємо тебе, ти — супергерой!</b>`,
        {
          parse_mode: 'HTML',
        }
      );
    }
  }

  static async broadcastDeclinedSuperhero(id) {
    if (id != 'undefined') {
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
}