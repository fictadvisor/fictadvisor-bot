import { Context } from 'telegraf';
import Action from './action.surrounder';
import { ApproveSuperhero } from './approve.superhero';
import { DenySuperhero } from './deny.superhero';

export class ActionsFactory {
  static create(name: string, ctx: Context): Action {
    const action: string = name.split(':')[0];

    const map = new Map([
      ['approve_superhero', ApproveSuperhero],
      ['deny_superhero', DenySuperhero]
    ]);

    if (map.has(action)) {
      const ActionClass = map.get(action);
      return new ActionClass(ctx);
    } else {
      return null;
    }
  }
}
