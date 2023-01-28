import TelegramService  from '../../../telegram/telegram.sevice';
import {escape} from 'html-escaper';
import {SuperheroDTO} from "./dto/superhero.dto";
import {superheroData} from "../../../callbacks/superhero";
import {Markup} from "telegraf";

export class SuperheroesService {
  static async broadcastPending(data: SuperheroDTO) {
    const bot = TelegramService.getInstance();
    const user = (await bot.telegram.getChat(data.telegramId)) as any;
    const chatId = process.env.CHAT_ID;
    await bot.telegram.sendMessage(chatId, `<b>Заявка на супергероя</b>\n\n` +
            `<b>Від:</b> ${data.firstName} ${data.middleName} ${data.lastName}\n\n` +
            `<b>Юзернейм:</b> <a href="tg://user?id=${user.id}">${user.username ? `@${user.username}` : `${user.first_name}`}</a>\n` +
            `<b>Група:</b> ${escape(data.groupCode)}\n` +
            `<b>Гуртожиток:</b> ${data.dorm ? 'так' : 'ні'}`,
    {
      parse_mode: 'HTML',
      ...Markup.inlineKeyboard([
        Markup.button.callback(
          "Схвалити",
          superheroData.create({
            method: "approve",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
        Markup.button.callback(
          "Відмовити",
          superheroData.create({
            method: "deny",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
      ]),
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