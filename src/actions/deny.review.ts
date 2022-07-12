import Action from './action.surrounder';
import api from '../api';

export class DenyReview extends Action {
  item_name = 'Відгук';

  createMessage (rawData): string {
    const data = rawData as {content: string, rating: number};

    return `<b>🔴 Відгук ${this.id} відхилено.</b>\n\n` +
        `<b>Відгук:</b> <pre>${data.content}</pre>\n` +
        `<b>Оцінка:</b> ${data.rating}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState (): Promise<object> {
    const obj = await api.reviews.update(this.id, { state: 'declined' });
    return obj.data;
  }
}
