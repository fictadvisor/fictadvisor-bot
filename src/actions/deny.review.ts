import Action from "./action.surrounder";
import api from "../api";

export class DenyReview extends Action {
  item_name = 'Відгук';

  createMessage(): string {
    return `<b>Відгук ${this.id} відхилено.</b>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<void> {
    await api.reviews.update(this.id, { state: 'declined' });
  }
}