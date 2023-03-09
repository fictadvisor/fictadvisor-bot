import { Context, Telegraf } from 'telegraf';

class TelegramService {
  private static bot: Telegraf<Context>;

  constructor() { }

  static getInstance(token?: string) {
    if (!TelegramService.bot) {
      this.bot = new Telegraf(token);
    }
    return this.bot;
  }
}
export default TelegramService;