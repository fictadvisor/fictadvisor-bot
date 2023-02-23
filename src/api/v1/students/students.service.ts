import TelegramService from '../../../telegram/telegram.sevice';
import {StudentDTO} from "./dto/student.dto";
import {studentData} from "../../../callbacks/student";
import {Markup} from "telegraf";

export class StudentsService {
  static async broadcastPending(data: StudentDTO) {
    const bot = TelegramService.getInstance();
    const user = (data.telegramId ? (await bot.telegram.getChat(data.telegramId)) as any : undefined);
    const chatId = data.captainTelegramId;
    await bot.telegram.sendMessage(chatId, `<b>Заявка на студента</b>\n\n` +
      `<b>Від:</b> ${data.lastName} ${data.firstName} ${data.middleName ? `${data.middleName}` : ``}\n` +
      (user ? `<b>Юзернейм:</b> <a href="tg://user?id=${user.id}">${user.username ? `@${user.username}` : `${user.first_name}`}</a>\n` : ``) +
      `<b>Група:</b> ${data.groupCode}`,
    {
      parse_mode: 'HTML',
      ...Markup.inlineKeyboard([
        Markup.button.callback(
          "Схвалити",
          studentData.pack({
            method: "approve",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
        Markup.button.callback(
          "Відмовити",
          studentData.pack({
            method: "deny",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
      ]),
    });
  }

  static async broadcastApprovedStudent(id) {
    if (id != 'undefined') {
      const bot = TelegramService.getInstance();
      await bot.telegram.sendMessage(
        id,
        `<b>Вітаємо тебе, ти — студент!</b>`,
        {
          parse_mode: 'HTML',
        }
      );
    }
  }

  static async broadcastDeclinedStudent(id) {
    if (id != 'undefined') {
      const bot = TelegramService.getInstance();
      await bot.telegram.sendMessage(
        id,
        `<b>На жаль, твій запит на студента було відхилено.</b>\n\n` +
        `Якщо в тебе є питання, звертайся до нас через бота зворотнього зв'язку: @fict_robot`,
        {
          parse_mode: 'HTML',
        }
      );
    }
  }
}