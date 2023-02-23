import {Router} from 'express';
import {ResponsesController} from './responses.controller';

const router = Router();

router.route('/broadcastPending').post(ResponsesController.broadcastPending);

export default router;