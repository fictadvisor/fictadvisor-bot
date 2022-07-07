import api from "../api";
import {ApproveAction} from "./approve.action";

export class ApproveTeacher extends ApproveAction {
  item_name = `Викладача`;

  createCallback(): string {
    return `deny_teacher:${this.id}`;
  }

  createMessage(): string {
    return `<b>Додавання викладача ${this.id} схвалено.</b>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<void> {
    await api.teachers.update(this.id, { state: 'approved' });
  }
}