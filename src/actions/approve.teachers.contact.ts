import api from '../api';
import { ApproveAction } from './approve.action';
import { TeacherContactDto } from '../api/dtos/teacher.contact.dto';

export class ApproveTeachersContact extends ApproveAction {
  item_name = 'Контакт викладача';

  createCallback(): string {
    return `deny_contact:${this.id}`;
  }

  createMessage(rawData): string {
    const data = rawData as TeacherContactDto;

    return `<b>🟢 Додавання контакту ${this.id} схвалено.</b>\n\n` +
        `<b>${data.name}:</b> ${data.value}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<object> {
    const obj = await api.contacts.update(this.id, { state: 'approved' });
    return obj.data;
  }
}
