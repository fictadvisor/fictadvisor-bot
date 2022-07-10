import { Context } from 'telegraf';
import { ApproveReview } from './approve.review';
import Action from './action.surrounder';
import { ApproveCourse } from './approve.course';
import { ApproveSubject } from './approve.subject';
import { ApproveTeacher } from './approve.teacher';
import { ApproveTeachersContact } from './approve.teachers.contact';
import { DenyReview } from './deny.review';
import { DenySubject } from './deny.subject';
import { DenyCourse } from './deny.course';
import { DenyTeacher } from './deny.teacher';
import { DenyTeachersContact } from './deny.teachers.contact';
import { ApproveSuperhero } from './approve.superhero';
import { DenySuperhero } from './deny.superhero';

export class ActionsFactory {
  static create (name: string, ctx: Context): Action {
    const action: string = name.split(':')[0];

    const map = new Map([
      ['approve_review', ApproveReview],
      ['approve_course', ApproveCourse],
      ['approve_subject', ApproveSubject],
      ['approve_teacher', ApproveTeacher],
      ['approve_contact', ApproveTeachersContact],
      ['approve_superhero', ApproveSuperhero],
      ['deny_review', DenyReview],
      ['deny_course', DenyCourse],
      ['deny_subject', DenySubject],
      ['deny_teacher', DenyTeacher],
      ['deny_contact', DenyTeachersContact],
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
