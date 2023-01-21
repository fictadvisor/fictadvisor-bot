import api from '../api';
import {ApproveAction} from './approve.action';
import {StudentDto} from '../api/dtos/student.dto';
import {StudentsService} from "../api/v1/students/students.service";

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

    async updateState(): Promise<object> {
        const obj = await api.superheroes.update(this.id, {state: 'approved'});
        await StudentsService.broadcastApprovedStudent(this.telegram_id)
        return obj.data;
    }
}
