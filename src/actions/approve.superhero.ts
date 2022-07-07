import api from "../api";
import {ApproveAction} from "./approve.action";

export class ApproveSuperhero extends ApproveAction {
  item_name = 'Супергероя';

  createCallback(): string {
    return `deny_superhero:${this.id}`;
  }

  createMessage(): string {
    return `<b>Заявка на супергероя ${this.id} схвалена.</b>\n\n` +
        `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
        `<b>Коли:</b> ${new Date().toISOString()}`;
  }

  async updateState(): Promise<void> {
    await api.superheroes.update(this.id, { state: 'approved' });
  }
}