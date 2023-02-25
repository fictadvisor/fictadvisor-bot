import TelegramService from "../../../telegram/telegram.sevice";
import {ResponseDto} from "./dto/response.dto";
import {Markup} from "telegraf";
import {responseData} from "../../../callbacks/response";
import * as process from "process";
import {UserAPI} from "../../user";

export class ResponsesService {
  static async broadcastPending(data: ResponseDto) {
    const bot = TelegramService.getInstance();
    const user = await UserAPI.getUser(data.userId);
    await bot.telegram.sendMessage(process.env.CHAT_ID,
      `<b>Відгук</b>\n\n`+
      `<b>QuestionId:</b> ${data.questionId}\n\n`+
      `<b>Предмет:</b> ${data.subject}\n` +
      `<b>Викладач:</b> ${data.teacherName}\n\n`+
      `<b>UserId:</b> ${data.userId}\n`+
      `<b>Від:</b> ${user.lastName} ${user.firstName} ${user.middleName ? `${user.middleName}` : ``}\n\n`+
      `<b>Відгук:</b> ${data.response}`,
      {
        parse_mode: 'HTML',
        ...Markup.inlineKeyboard([
          Markup.button.callback(
            "Схвалити",
            responseData.pack({
              method: "approve",
              id: data.disciplineTeacherId,
            })
          ),
          Markup.button.callback(
            "Відмовити",
            responseData.pack({
              method: "deny",
              id: data.disciplineTeacherId,
            })
          ),
        ]),
      });
  }
}