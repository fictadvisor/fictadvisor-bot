import api from '../api';
import { ApproveAction } from './approve.action';

export class ApproveCourse extends ApproveAction {
  item_name = 'Курс';

  createCallback (): string {
    return `deny_course:${this.id}`;
  }

  createMessage (): string {
    return `<b>🟢 Додавання курсу ${this.id} схвалено.</b>\n\n` +
      `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
      `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState (): Promise<object> {
    const obj = await api.courses.update(this.id, { state: 'approved' });
    return obj.data;
  }
}
