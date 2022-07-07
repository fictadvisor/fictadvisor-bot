import Action from "./action.surrounder";
import api from "../api";

export class DenyTeacher extends Action {
  item_name = 'Викладача';

  createMessage(): string {
    return `<b>Додавання викладача ${this.id} відхилено.</b>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<void> {
    await api.teachers.update(this.id, { state: 'declined' });
  }
}