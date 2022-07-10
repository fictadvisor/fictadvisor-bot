import { Context } from 'telegraf'
import { Message, User } from 'telegraf/typings/core/types/typegram'
import { AxiosError } from 'axios'

const PARSE_HTML_OBJECT = {
  parse_mode: 'HTML',
}

export default abstract class Action {
  item_name: string
  context: Context

  constructor (ctx: Context) {
    this.context = ctx
  }

  get from ():User {
    return this.context.callbackQuery.from
  }

  get id (): string {
    return (this.context.callbackQuery as any).data.split(':')[1]
  }

  get message (): Message.CommonMessage {
    return this.context.callbackQuery.message
  }

  get inline_message_id (): string {
    return this.context.callbackQuery.inline_message_id
  }

  get ctx () {
    return this.context
  }

  async execute (): Promise<void> {
    await this.updateState()

    const extra: object = Object.assign({}, PARSE_HTML_OBJECT);

    this.addMarkup(extra)

    await this.ctx.telegram.editMessageText(
      this.message.chat.id,
      this.message.message_id,
      this.inline_message_id,
      this.createMessage(),
      extra
    )
  }

  async catch (e) {
    const axiosError = e as AxiosError

    if (axiosError.isAxiosError) {
      if (axiosError.response?.status === 404) {
        await this.ctx.telegram.editMessageText(
          this.message.chat.id,
          this.message.message_id,
          this.inline_message_id,
          `<b>🔴 ${this.item_name} ${this.id} вже було видалено.</b>`,
          Object.assign({}, PARSE_HTML_OBJECT),
        )

        return
      }
    }

    console.error(e)
    await this.ctx.reply(e.toString(), { reply_to_message_id: this.message.message_id })
  }

  abstract createMessage(): string;

  abstract updateState(): Promise<void>;

  addMarkup (extra: object) {}
}
