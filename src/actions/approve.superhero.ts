import { ApproveAction } from './approve.action';
import {SuperheroesService} from "../api/v1/superheroes/superheroes.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";
import {superheroData} from "../callbacks/superhero";

export class ApproveSuperhero extends ApproveAction {
  item_name = 'Супергероя';

  createCallback(): string {
    return superheroData.create({
      method: "deny",
      id: this.id,
      telegramId: this.telegram_id,
    });
  }

  createMessage(): string {

    return `<b>🟢 Заявка на супергероя ${this.id} схвалена.</b>\n\n` +
        `<b>Нікнейм:</b> <a href="tg://user?id=${this.user.id}">${this.user.username ?
          `@${this.user.username}` : this.user.first_name}</a>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(){
    await UserAPI.verifySuperhero(this.id, State.APPROVED);
    await SuperheroesService.broadcastApprovedSuperhero(this.telegram_id);
  }
}
