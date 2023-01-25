import { ApproveAction } from './approve.action';
import { SuperheroDto } from '../api/dtos/superhero.dto';
import {SuperheroesService} from "../api/v1/superheroes/superheroes.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";

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

  async updateState(){
    await UserAPI.verifySuperhero(this.id, State.APPROVED);
    await SuperheroesService.broadcastApprovedSuperhero(this.telegram_id);
  }
}
