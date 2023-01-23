import {Context} from 'telegraf';
import Action from './action.surrounder';
import {ApproveSuperhero} from './approve.superhero';
import {DenySuperhero} from './deny.superhero';
import {ApproveCaptain} from './approve.captain';
import {DenyCaptain} from './deny.captain';
import {ApproveStudent} from './approve.student';
import {DenyStudent} from './deny.student';

export class ActionsFactory {
  static create(name: string, ctx: Context): Action {
    const action: string = name.split(':')[0];

    const map = new Map([
      ['approve_superhero', ApproveSuperhero],
      ['deny_superhero', DenySuperhero],
      ['approve_captain', ApproveCaptain],
      ['deny_captain', DenyCaptain],
      ['approve_student', ApproveStudent],
      ['deny_student', DenyStudent],
    ]);

    if (map.has(action)) {
      const ActionClass = map.get(action);
      return new ActionClass(ctx);
    } else {
      return null;
    }
  }
}
