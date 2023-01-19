import { TeachersService } from './teachers.service';

export class TeachersController {
    static async broadcastPending(req, res) {
        try {
            const data = TeachersService.broadcastPending(req.body);
            return res.status(200).send({message: data});
        } catch(err) {
            return res.status(400).send({message: 'Xyina'});
        }
    }

}