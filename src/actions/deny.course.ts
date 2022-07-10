import Action from './action.surrounder';
import api from '../api';

export class DenyCourse extends Action {
  item_name = 'Курс';

  createMessage (data: {name: string}): string {
    return `<b>🔴 Додавання курсу ${this.id} відхилено.</b>\n\n` +
        `<b>Назва курсу:</b> ${data.name}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState (): Promise<object> {
    const obj = await api.courses.update(this.id, { state: 'declined' });
    return obj.data;
  }
}
