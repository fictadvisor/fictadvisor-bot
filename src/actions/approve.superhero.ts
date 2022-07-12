import api from '../api';
import { ApproveAction } from './approve.action';
import { SuperheroDto } from '../api/dtos/superhero.dto';

export class ApproveSuperhero extends ApproveAction {
  item_name = 'Супергероя';

  createCallback(): string {
    return `deny_superhero:${this.id}`;
  }

  createMessage(rawData): string {
    const data = rawData as SuperheroDto;

    return `<b>🟢 Заявка на супергероя ${this.id} схвалена.</b>\n\n` +
        `<b>Нікнейм:</b> @${data.username}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<object> {
    const obj = await api.superheroes.update(this.id, { state: 'approved' });
    return obj.data;
  }
}
