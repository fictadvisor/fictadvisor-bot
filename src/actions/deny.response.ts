import Action from "./action.surrounder";
import {ExtraEditMessageText} from "telegraf/typings/telegram-types";
import {ParseMode} from "typegram/message";

const PARSE_HTML_OBJECT = {
  parse_mode: 'HTML' as ParseMode,
};

export class DenyResponse extends Action {
  get discipline_teacher_id(): string {
    return (this.context.callbackQuery as any).data.split(':')[1];
  }

  createMessage(): string {
    return (this.ctx.callbackQuery.message as any).text.replace(`Відгук`, `🔴 Відгук ${this.discipline_teacher_id} схвалено`);
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

  async updateState() {
    return;
  }
}