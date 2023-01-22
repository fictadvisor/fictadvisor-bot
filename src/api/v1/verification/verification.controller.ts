import { VerificationCaptainService } from './verficationCaptain.service';
import { VerificationStudentService } from './verficationStudent.service';

export class VerificationController {
  static async verifyCaptain(req, res) {
    try {
      const data = VerificationCaptainService.verifyCaptain(req.body);
      return res.status(200).send({message: data});
    } catch(err) {
      return res.status(400).send({message: 'An exception occured while sending message'});
    }
  }
  
  static async verifyStudent(req, res) {
    try {
      const data = VerificationStudentService.verifyStudent(req.body);
      return res.status(200).send({message: data});
    } catch(err) {
      return res.status(400).send({message: 'An exception occured while sending message'});
    }
  }
}