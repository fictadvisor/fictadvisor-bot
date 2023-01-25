import {ApproveAction} from './approve.action';
import {CaptainDto} from '../api/dtos/captain.dto';
import {CaptainsService} from "../api/v1/captains/captains.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";

export class ApproveCaptain extends ApproveAction {
  item_name = 'Старосту';

  createCallback(): string {
    return `deny_captain:${this.id}`;
  }

  createMessage(rawData): string {
    const data = rawData as CaptainDto;

    return `<b>🟢 Заявка на старосту ${this.id} схвалена.</b>\n\n` +
            `<b>Нікнейм:</b> @${data.username}\n\n` +
            `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ?
              `@${this.from.username}` : this.from.first_name}</a>\n` +
            `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState() {
    await UserAPI.verifyStudent(this.id, State.APPROVED);
    await CaptainsService.broadcastApprovedCaptain(this.telegram_id);
  }
}
