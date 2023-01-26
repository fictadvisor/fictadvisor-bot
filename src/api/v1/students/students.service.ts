import TelegramService from '../../../telegram/telegram.sevice';
import {escape} from 'html-escaper';
import {StudentDTO} from "./dto/student.dto";
import {studentData} from "../../../callbacks/student";
import {Markup} from "telegraf";

export class StudentsService {
  static async broadcastPending(data: StudentDTO) {
    const bot = TelegramService.getInstance();
    const user = (await bot.telegram.getChat(data.telegramId)) as any;
    const chatId = process.env.CHAT_ID;
    await bot.telegram.sendMessage(chatId, `<b>Заявка на студента</b>\n\n` +
      `<b>Від:</b> ${data.firstName} ${data.middleName} ${data.lastName}\n\n` +
      `<b>Юзернейм:</b> <a href="tg://user?id=${user.id}">${user.username ? `@${user.username}` : `${user.first_name}`}</a>\n` +
      `<b>Група:</b> ${escape(data.groupCode)}`,
    {
      parse_mode: 'HTML',
      ...Markup.inlineKeyboard([
        Markup.button.callback(
          "Схвалити",
          studentData.create({
            method: "approve",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
        Markup.button.callback(
          "Відмовити",
          studentData.create({
            method: "deny",
            id: data.id,
            telegramId: String(data.telegramId),
          })
        ),
      ]),
    });
  }

  static async broadcastApprovedStudent(id) {
    const bot = TelegramService.getInstance();
    await bot.telegram.sendMessage(
      id,
      `<b>Вітаємо тебе, ти — студент!</b>`,
      {
        parse_mode: 'HTML',
      }
    );
  }

  static async broadcastDeclinedStudent(id) {
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