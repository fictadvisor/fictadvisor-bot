import api from '../api';
import { ApproveAction } from './approve.action';
import { TeacherDto } from '../api/dtos/teacher.dto';

export class ApproveTeacher extends ApproveAction {
  item_name = 'Викладача';

  createCallback(): string {
    return `deny_teacher:${this.id}`;
  }

  createMessage(rawData): string {
    const data = rawData as TeacherDto;

    return `<b>🟢 Додавання викладача ${this.id} схвалено.</b>\n\n` +
        `<b>ПІБ Викладача:</b> ${data.lastName} ${data.firstName} ${data.middleName}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<object> {
    const obj = await api.teachers.update(this.id, { state: 'approved' });
    return obj.data;
  }
}
