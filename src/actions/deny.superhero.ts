import Action from "./action.surrounder";
import api from "../api";

export class DenySuperhero extends Action {
  item_name = 'Супергероя';

  createMessage(): string {
    return `<b>Додавання супергероя ${this.id} відхилено.</b>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<void> {
    await api.superheroes.update(this.id, { state: 'hidden' });
  }
}