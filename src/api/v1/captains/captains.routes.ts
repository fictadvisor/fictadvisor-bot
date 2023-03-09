import {Router} from 'express';
import {CaptainsController} from './captains.controller';

const router = Router();

router.route('/broadcastPending').post(CaptainsController.broadcastPending);

export default router;