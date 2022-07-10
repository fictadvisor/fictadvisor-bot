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
    let ActionClass = null;

    switch (action) {
      case 'approve_review': ActionClass = ApproveReview; break;
      case 'approve_course': ActionClass = ApproveCourse; break;
      case 'approve_subject': ActionClass = ApproveSubject; break;
      case 'approve_teacher': ActionClass = ApproveTeacher; break;
      case 'approve_contact': ActionClass = ApproveTeachersContact; break;
      case 'approve_superhero': ActionClass = ApproveSuperhero; break;
      case 'deny_review': ActionClass = DenyReview; break;
      case 'deny_course': ActionClass = DenyCourse; break;
      case 'deny_subject': ActionClass = DenySubject; break;
      case 'deny_teacher': ActionClass = DenyTeacher; break;
      case 'deny_contact': ActionClass = DenyTeachersContact; break;
      case 'deny_superhero': ActionClass = DenySuperhero; break;
    }

    if (ActionClass !== null) {
      return new ActionClass(ctx);
    } else {
      return null;
    }
  }
}
