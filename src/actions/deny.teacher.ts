import Action from './action.surrounder';
import api from '../api';
import { TeacherDto } from '../api/dtos/teacher.dto';

export class DenyTeacher extends Action {
  item_name = 'Викладача';

  createMessage(rawData): string {
    const data = rawData as TeacherDto;

    return `<b>🔴 Додавання викладача ${this.id} відхилено.</b>\n\n` +
        `<b>ПІБ Викладача:</b> ${data.last_name} ${data.first_name} ${data.middle_name}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<object> {
    const obj = await api.teachers.update(this.id, { state: 'declined' });
    return obj.data;
  }
}
