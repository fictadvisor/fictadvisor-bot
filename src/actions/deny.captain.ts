import Action from './action.surrounder';
import api from '../api';
import {CaptainDto} from '../api/dtos/captain.dto';
import {CaptainsService} from "../api/v1/captains/captains.service";

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

    async updateState(): Promise<object> {
        const obj = await api.superheroes.update(this.id, {state: 'hidden'});
        await CaptainsService.broadcastDeclinedCaptain(this.telegram_id);
        return obj.data;
    }
}
