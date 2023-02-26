import Action from './action.surrounder';
import {SuperheroesService} from "../api/v1/superheroes/superheroes.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";

export class DenySuperhero extends Action {
  item_name = 'Супергероя';

  createMessage(): string {

    return `<b>🔴 Додавання супергероя ${this.id} відхилено.</b>\n\n` +
        `<b>ПІБ:</b> ${this.student.lastName} ${this.student.firstName} ${this.student.middleName ? `${this.student.middleName}` : ``}\n` +
        `<b>Група:</b> ${this.student.group.code}\n` +
        (this.user ? `<b>Нікнейм:</b> <a href="tg://user?id=${this.user.id}">${this.user.username ? `@${this.user.username}` : `${this.user.first_name}`}</a>\n\n` : `\n`) +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState() {
    await UserAPI.verifySuperhero(this.id, State.DECLINED);
    await SuperheroesService.broadcastDeclinedSuperhero(this.telegram_id);
  }
}
