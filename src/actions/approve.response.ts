import Action from "./action.surrounder";
import {ExtraEditMessageText} from "telegraf/typings/telegram-types";
import {ParseMode} from "typegram/message";
import {ResponseApi} from "../api/response";

const PARSE_HTML_OBJECT = {
  parse_mode: 'HTML' as ParseMode,
};

export class ApproveResponse extends Action {
  get discipline_teacher_id(): string {
    return (this.context.callbackQuery as any).data.split(':')[1];
  }

  async execute(): Promise<void> {
    await this.updateState();
    const extra: ExtraEditMessageText = Object.assign({}, PARSE_HTML_OBJECT);

    this.addMarkup(extra);

    await this.ctx.telegram.editMessageText(
      this.message.chat.id,
      this.message.message_id,
      this.inline_message_id,
      this.createMessage(),
      extra
    );
  }

  createMessage(): string {
    return (this.ctx.callbackQuery.message as any).text.replace(`Відгук`, `🟢 Відгук ${this.discipline_teacher_id} схвалено`);
  }

  async updateState() {
    await ResponseApi.verifyResponse(this.discipline_teacher_id, {
      userId: (this.ctx.callbackQuery.message as any).text.match(/userId:\s+.*/)[0].split(`userId: `)[1],
      questionId: (this.ctx.callbackQuery.message as any).text.match(/^questionId:\s+.*/)[0].split(`questionId: `)[1],
      value: (this.ctx.callbackQuery.message as any).text.match(/Відгук:\s+.*/s)[0].split(`Відгук: `)[1],
    });
  }
}