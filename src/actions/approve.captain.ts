import {ApproveAction} from './approve.action';
import {CaptainsService} from "../api/v1/captains/captains.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";
import {captainData} from "../callbacks/captain";

export class ApproveCaptain extends ApproveAction {
  item_name = 'Старосту';

  createCallback(): string {
    return captainData.pack({
      method: "deny",
      id: this.id,
      telegramId: this.telegram_id,
    });
  }

  createMessage(): string {

    return `<b>🟢 Заявка на старосту ${this.id} схвалена.</b>\n\n` +
            `<b>ПІБ:</b> ${this.student.lastName} ${this.student.firstName} ${this.student.middleName ? `${this.student.middleName}` : ``}\n` +
            `<b>Група:</b> ${this.student.groupCode}\n` +
            (this.user ? `<b>Нікнейм:</b> <a href="tg://user?id=${this.user.id}">${this.user.username ? `@${this.user.username}` : `${this.user.first_name}`}</a>\n\n` : `\n`) +
            `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ?
              `@${this.from.username}` : this.from.first_name}</a>\n` +
            `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState() {
    await UserAPI.verifyStudent(this.id, State.APPROVED, true);
    await CaptainsService.broadcastApprovedCaptain(this.telegram_id);
  }
}
