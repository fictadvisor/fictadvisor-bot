import { Context } from 'telegraf';
import { Message, User } from 'telegraf/typings/core/types/typegram';
import { AxiosError } from 'axios';
import { ExtraEditMessageText } from 'telegraf/typings/telegram-types';
import { ParseMode } from 'typegram/message';
import {UserAPI} from "../api/user";

const PARSE_HTML_OBJECT = {
  parse_mode: 'HTML' as ParseMode,
};

export default abstract class Action {
  item_name: string;
  user: any;
  student: any;
  protected context: Context;

  constructor(ctx: Context) {
    this.context = ctx;
  }

  get from():User {
    return this.context.callbackQuery.from;
  }

  get id(): string {
    console.log((this.context.callbackQuery as any).data);
    return (this.context.callbackQuery as any).data.split(':')[2];
  }

  get telegram_id(): string {
    return (this.context.callbackQuery as any).data.split(':')[3];
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
    await this.updateState();
    this.user = (this.telegram_id != 'undefined' ? await this.context.tg.getChat(this.telegram_id) : undefined);
    this.student = await UserAPI.getUser(this.id);
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

  abstract createMessage(): string;

  abstract updateState();

  addMarkup(extra: object) {}
}
