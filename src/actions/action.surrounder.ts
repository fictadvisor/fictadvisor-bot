import { Context } from 'telegraf';
import { Message, User } from 'telegraf/typings/core/types/typegram';
import { AxiosError } from 'axios';
import { ExtraEditMessageText } from 'telegraf/typings/telegram-types';
import { ParseMode } from 'typegram/message';

const PARSE_HTML_OBJECT = {
  parse_mode: 'HTML' as ParseMode
};

export default abstract class Action {
  item_name: string;
  protected context: Context;

  constructor(ctx: Context) {
    this.context = ctx;
  }

  get from():User {
    return this.context.callbackQuery.from;
  }

  get id(): string {
    return (this.context.callbackQuery as any).data.split(':')[1];
  }

  get message(): Message.CommonMessage {
    return this.context.callbackQuery.message;
  }

  get inline_message_id(): string {
    return this.context.callbackQuery.inline_message_id;
  }

  get ctx() {
    return this.context;
  }

  async execute(): Promise<void> {
    const data = await this.updateState();
    const extra: ExtraEditMessageText = Object.assign({}, PARSE_HTML_OBJECT);

    this.addMarkup(extra);

    await this.ctx.telegram.editMessageText(
      this.message.chat.id,
      this.message.message_id,
      this.inline_message_id,
      this.createMessage(data),
      extra
    );
  }

  async catch(e) {
    const axiosError = e as AxiosError;

    if (axiosError.isAxiosError) {
      if (axiosError.response?.status === 404) {
        await this.ctx.telegram.editMessageText(
          this.message.chat.id,
          this.message.message_id,
          this.inline_message_id,
          `<b>🔴 ${this.item_name} ${this.id} вже було видалено.</b>`,
          Object.assign({}, PARSE_HTML_OBJECT) as ExtraEditMessageText
        );

        return;
      }
    }

    console.error(e);
    await this.ctx.reply(e.toString(), { reply_to_message_id: this.message.message_id });
  }

  abstract createMessage(data: object): string;

  abstract updateState(): Promise<object>;

  addMarkup(extra: object) {}
}
