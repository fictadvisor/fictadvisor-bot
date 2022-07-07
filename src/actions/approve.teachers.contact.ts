import api from "../api";
import {ApproveAction} from "./approve.action";

export class ApproveTeachersContact extends ApproveAction {
  item_name = 'Контакт викладача';

  createCallback(): string {
    return `deny_contact:${this.id}`;
  }

  createMessage(): string {
    return `<b>Додавання контакту ${this.id} схвалено.</b>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<void> {
    await api.contacts.update(this.id, { state: 'approved' });
  }
}