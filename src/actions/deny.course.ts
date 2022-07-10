import Action from './action.surrounder';
import api from '../api';

export class DenyCourse extends Action {
  item_name = 'Курс';

  createMessage (data: {name: string, teacher: {first_name: string, middle_name: string, last_name: string}}): string {
    return `<b>🔴 Додавання курсу ${this.id} відхилено.</b>\n\n` +
        `<b>Назва курсу:</b> ${data.name}\n` +
        `<b>ПІБ Викладача:</b> ${data.teacher.last_name} ${data.teacher.first_name} ${data.teacher.middle_name}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState (): Promise<object> {
    const obj = await api.courses.update(this.id, { state: 'declined' });
    return obj.data;
  }
}
