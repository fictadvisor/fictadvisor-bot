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
      `Відгук\n\n`+
      `questionId: ${data.questionId}\n\n`+
      `Предмет: ${data.subject}\n` +
      `Викладач: ${data.teacherName}\n\n`+
      `userId: ${data.userId}\n`+
      `Від: ${user.lastName} ${user.firstName} ${user.middleName ? `${user.middleName}` : ``}\n\n`+
      `Відгук: ${data.response}`,
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