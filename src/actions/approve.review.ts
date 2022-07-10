import api from '../api'
import { ApproveAction } from './approve.action'

export class ApproveReview extends ApproveAction {
  item_name = 'Відгук'

  createCallback (): string {
    return `deny_review:${this.id}`
  }

  createMessage (): string {
    return `<b>🟢 Відгук ${this.id} схвалено.</b>\n\n` +
      `<b>Ким:</b> <a href="tg://user?id=${this.from.id}">${this.from.username ? `@${this.from.username}` : this.from.first_name}</a>\n` +
      `<b>Коли:</b> ${new Date().toISOString()}`
  }

  async updateState (): Promise<void> {
    await api.reviews.update(this.id, { state: 'approved' })
  }
}
