import Action from "./action.surrounder";

export abstract class ApproveAction extends Action {
  abstract createCallback();

  addMarkup(extra): void {
    extra.inline_keyboard = [
      [{ text: 'Скасувати та видалити', callback_data: this.createCallback() }]
    ]
  }
}

