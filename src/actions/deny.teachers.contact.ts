import Action from './action.surrounder';
import api from '../api';

export class DenyTeachersContact extends Action {
  item_name = 'Контакт викладача';

  createMessage (): string {
    return `<b>🔴 Додавання контакту викладача ${this.id} відхилено.</b>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState (): Promise<object> {
    const obj = await api.contacts.update(this.id, { state: 'declined' });
    return obj.data;
  }
}
