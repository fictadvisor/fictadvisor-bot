import api from '../api';
import { ApproveAction } from './approve.action';
import { SubjectDto } from '../api/dtos/subject.dto';

export class ApproveSubject extends ApproveAction {
  item_name = 'Предмет';

  createCallback(): string {
    return `deny_subject:${this.id}`;
  }

  createMessage(rawData: {name: string}): string {
    const data = rawData as SubjectDto;

    return `<b>🟢 Додавання предмету ${this.id} схвалено.</b>\n\n` +
        `<b>Назва предмету</b>: ${data.name}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<object> {
    const obj = await api.subjects.update(this.id, { state: 'approved' });
    return obj.data;
  }
}
