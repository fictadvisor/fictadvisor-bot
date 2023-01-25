import {ApproveAction} from './approve.action';
import {StudentDto} from '../api/dtos/student.dto';
import {StudentsService} from "../api/v1/students/students.service";
import {UserAPI} from "../api/user";
import {State} from "../api/state";

export class ApproveStudent extends ApproveAction {
  item_name = 'Старосту';

  createCallback(): string {
    return `deny_student:${this.id}`;
  }

  createMessage(rawData): string {
    const data = rawData as StudentDto;

    return `<b>🟢 Заявка на студента ${this.id} схвалена.</b>\n\n` +
            `<b>Нікнейм:</b> @${data.username}\n\n` +
            `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ?
              `@${this.from.username}` : this.from.first_name}</a>\n` +
            `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState() {
    await UserAPI.verifyStudent(this.id, State.APPROVED);
    await StudentsService.broadcastApprovedStudent(this.telegram_id);
  }
}
