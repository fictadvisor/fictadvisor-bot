import { Context } from "telegraf";
import { Message, User } from "telegraf/typings/core/types/typegram";
import { AxiosError } from "axios";

export default abstract class Action {
  id: string;
  message: Message.CommonMessage;
  inline_message_id: string;
  from: User;
  item_name: string;

  set ctx (ctx: Context) {
    this.id = (ctx.callbackQuery as any).data.split(':')[1];
    this.message = ctx.callbackQuery.message;
    this.inline_message_id = ctx.callbackQuery.inline_message_id;
    this.from = ctx.callbackQuery.from;
  }

  async execute(): Promise<void> {
    await this.updateState();

    const extra: object = {
      parse_mode: 'HTML',
    }

    this.addMarkup(extra);

    await this.ctx.telegram.editMessageText(
        this.message.chat.id,
        this.message.message_id,
        this.inline_message_id,
        this.createMessage(),
        extra,
    )
  }

  async catch(e) {
    const axiosError = e as AxiosError;

    if (axiosError.isAxiosError) {
      if (axiosError.response?.status === 404) {
        await this.ctx.telegram.editMessageText(
            this.message.chat.id,
            this.message.message_id,
            this.inline_message_id,
            `<b>${this.item_name} ${this.id} вже було видалено.</b>`,
            {
              parse_mode: 'HTML',
            }
        );

        return;
      }
    }

    console.error(e);
    await this.ctx.reply(e.toString(), {reply_to_message_id: this.message.message_id});
  }

  abstract createMessage(): string;

  abstract updateState(): Promise<void>;

  addMarkup(extra: object) {}
}

