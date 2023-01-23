import {Router} from 'express';
import {StudentsController} from './students.controller';

const router = Router();

router.route('/broadcastPending').post(StudentsController.broadcastPending);

export default router;