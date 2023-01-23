import Action from './action.surrounder';
import api from '../api';
import {StudentDto} from '../api/dtos/student.dto';
import {StudentsService} from "../api/v1/students/students.service";

export class DenyStudent extends Action {
  item_name = 'Студента';

  createMessage(rawData): string {
    const data = rawData as StudentDto;

    return `<b>🔴 Додавання студента ${this.id} відхилено.</b>\n\n` +
            `<b>Нікнейм:</b> @${data.username}\n\n` +
            `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ?
              `@${this.from.username}` : this.from.first_name}</a>\n` +
            `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<object> {
    const obj = await api.superheroes.update(this.id, {state: 'hidden'});
    await StudentsService.broadcastDeclinedStudent(this.telegram_id);
    return obj.data;
  }
}
