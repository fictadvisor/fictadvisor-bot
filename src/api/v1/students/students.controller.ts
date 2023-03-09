import {StudentsService} from './students.service';

export class StudentsController {
  static async broadcastPending(req, res) {
    try {
      const data = await StudentsService.broadcastPending(req.body);
      return res.status(200).send({message: data});
    } catch (err) {
      return res.status(400).send({message: 'An exception occurred while sending message'});
    }
  }
}