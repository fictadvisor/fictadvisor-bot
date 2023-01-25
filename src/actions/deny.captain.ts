import Action from './action.surrounder';
import {CaptainDto} from '../api/dtos/captain.dto';
import {CaptainsService} from "../api/v1/captains/captains.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";

export class DenyCaptain extends Action {
  item_name = 'Старосту';

  createMessage(rawData): string {
    const data = rawData as CaptainDto;

    return `<b>🔴 Додавання старости ${this.id} відхилено.</b>\n\n` +
            `<b>Нікнейм:</b> @${data.username}\n\n` +
            `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ?
              `@${this.from.username}` : this.from.first_name}</a>\n` +
            `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState() {
    await UserAPI.verifyStudent(this.id, State.DECLINED);
    await CaptainsService.broadcastDeclinedCaptain(this.telegram_id);
  }
}
