import { TeachersService } from './teachers.service';

export class TeachersController {
    static async broadcastPending(req, res) {
        const data = TeachersService.broadcastPending(req.body);
        return res.status(200).send({message: data});
    }
}