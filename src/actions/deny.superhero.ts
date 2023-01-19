import Action from './action.surrounder';
import api from '../api';
import { SuperheroDto } from '../api/dtos/superhero.dto';
import {SuperheroesService} from "../api/v1/superheroes/superheroes.service";

export class DenySuperhero extends Action {
  item_name = 'Супергероя';

  createMessage(rawData): string {
    const data = rawData as SuperheroDto;

    return `<b>🔴 Додавання супергероя ${this.id} відхилено.</b>\n\n` +
        `<b>Нікнейм:</b> @${data.username}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<object> {
    const obj = await api.superheroes.update(this.id, { state: 'hidden' });
    await SuperheroesService.broadcastDeclinedSuperhero(this.telegram_id);
    return obj.data;
  }
}
