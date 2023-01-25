import Action from './action.surrounder';
import { SuperheroDto } from '../api/dtos/superhero.dto';
import {SuperheroesService} from "../api/v1/superheroes/superheroes.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";

export class DenySuperhero extends Action {
  item_name = 'Супергероя';

  createMessage(rawData): string {
    const data = rawData as SuperheroDto;

    return `<b>🔴 Додавання супергероя ${this.id} відхилено.</b>\n\n` +
        `<b>Нікнейм:</b> @${data.username}\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState() {
    await UserAPI.verifySuperhero(this.id, State.DECLINED);
    await SuperheroesService.broadcastDeclinedSuperhero(this.telegram_id);
  }
}
