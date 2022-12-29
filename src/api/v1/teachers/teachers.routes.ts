import { Router } from 'express';
import { TeachersController } from './teachers.controller';

const router = Router();

router.route('/broadcastPending').post(TeachersController.broadcastPending)

export default router;